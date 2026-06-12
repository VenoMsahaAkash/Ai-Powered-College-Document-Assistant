import os
import numpy as np
from typing import List, Tuple
from pathlib import Path

from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from sentence_transformers import SentenceTransformer
import faiss


class RAGPipeline:

    def __init__(
        self,
        api_key: str = None,
        chunk_size: int = 500,
        chunk_overlap: int = 50,
        embedding_model: str = "all-MiniLM-L6-v2",
        top_k: int = 4,
    ):
        # Load API key from .env file automatically
        from dotenv import load_dotenv
        import os

        load_dotenv()

        try:
            import streamlit as st
            api_key = (
                api_key
                or st.secrets.get("GOOGLE_API_KEY", "")
                or os.getenv("GOOGLE_API_KEY", "")
                    )
        except Exception:
            api_key = api_key or os.getenv("GOOGLE_API_KEY", "")

        if not api_key:
            raise ValueError("No API key found. Add GOOGLE_API_KEY to your .env file.")

        self.api_key = api_key
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.top_k = top_k

        # Text Splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ". ", " ", ""],
        )

        # Embedding Model (runs locally, no API cost)
        print(f"⏳ Loading embedding model: {embedding_model} ...")
        self.embedder = SentenceTransformer(embedding_model)
        self.embedding_dim = self.embedder.get_sentence_embedding_dimension()
        print(f"✅ Embedding model loaded. Vector size: {self.embedding_dim}")

        # Gemini LLM
        os.environ["GOOGLE_API_KEY"] = api_key

        self.llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.3,
        google_api_key=api_key,
)

        # FAISS Index (created during build_index)
        self.index = None
        self.chunks = []
        self.chunk_metadata = []

    def build_index(self, file_paths: List[str]) -> int:
        all_chunks = []
        all_metadata = []

        for path in file_paths:
            print(f"\n📄 Processing: {path}")
            raw_docs = self._load_document(path)
            chunks = self.text_splitter.split_documents(raw_docs)

            for chunk in chunks:
                all_chunks.append(chunk.page_content)
                all_metadata.append({
                    "source": os.path.basename(path),
                    "page": chunk.metadata.get("page", 0),
                })

        if not all_chunks:
            raise ValueError("No text could be extracted from the uploaded files.")

        print(f"\n✂️  Total chunks created: {len(all_chunks)}")
        print("🔢 Creating embeddings...")

        embeddings = self.embedder.encode(
            all_chunks,
            show_progress_bar=True,
            convert_to_numpy=True,
        )

        faiss.normalize_L2(embeddings)

        self.index = faiss.IndexFlatIP(self.embedding_dim)
        self.index.add(embeddings.astype(np.float32))

        self.chunks = all_chunks
        self.chunk_metadata = all_metadata

        print(f"✅ FAISS index built with {self.index.ntotal} vectors.")
        return len(all_chunks)

    def query(self, question: str) -> Tuple[str, List[str]]:
        if self.index is None:
            raise RuntimeError("No index built yet. Call build_index() first.")

        q_embedding = self.embedder.encode([question], convert_to_numpy=True)
        faiss.normalize_L2(q_embedding)

        distances, indices = self.index.search(
            q_embedding.astype(np.float32), self.top_k
        )

        retrieved_chunks = []
        retrieved_sources = []
        for idx, dist in zip(indices[0], distances[0]):
            if idx == -1:
                continue
            chunk_text = self.chunks[idx]
            meta = self.chunk_metadata[idx]
            retrieved_chunks.append(chunk_text)
            retrieved_sources.append(
                f"[{meta['source']} | Page {meta['page']+1}] {chunk_text[:200]}..."
            )

        context = "\n\n---\n\n".join(retrieved_chunks)

        system_prompt = """You are a helpful assistant for college students.
Answer questions using ONLY the context provided below.
If the answer is not in the context, say "I couldn't find that information in the uploaded documents."
Be clear, concise, and student-friendly."""

        user_prompt = f"""Context from college documents:
{context}

Question: {question}

Answer based only on the context above:"""

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt),
        ]
        import time
        for attempt in range(3):
            try:
                response = self.llm.invoke(messages)
                break
            except Exception as e:
                if "429" in str(e) and attempt < 2:
                    wait = 60 * (attempt + 1)
                    print(f"⏳ Quota hit, waiting {wait}s before retry...")
                    time.sleep(wait)
                else:
                    raise
        return response.content, retrieved_sources

    def _load_document(self, file_path: str):
        ext = Path(file_path).suffix.lower()

        if ext == ".pdf":
            loader = PyPDFLoader(file_path)
        elif ext == ".txt":
            loader = TextLoader(file_path, encoding="utf-8")
        else:
            raise ValueError(f"Unsupported file type: {ext}. Use PDF or TXT.")

        docs = loader.load()
        print(f"  → Loaded {len(docs)} page(s) / section(s)")
        return docs
