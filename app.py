import streamlit as st
import os
from pathlib import Path
from rag_pipeline import RAGPipeline

st.set_page_config(
    page_title="College Document Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)
import base64

def get_base64_image(image_path):
    with open(image_path, "rb") as img:
        return base64.b64encode(img.read()).decode()

bg_image = get_base64_image("assets/college_bg.jpg")

st.markdown(
    f"""
    <style>

    [data-testid="stAppViewContainer"] {{
        background-image: url("data:image/jpeg;base64,{bg_image}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}

    [data-testid="stAppViewContainer"] > .main {{
        background: rgba(0,0,0,0.35);
    }}

    [data-testid="stHeader"] {{
        background: transparent;
    }}

    [data-testid="stSidebar"] {{
        background: rgba(15,23,42,0.88);
        backdrop-filter: blur(10px);
    }}

    .block-container {{
        padding-top: 2rem;
    }}

    h1, h2, h3, p, label {{
        color: white !important;
    }}

    .metric-card {{
        background: rgba(255,255,255,0.12);
        backdrop-filter: blur(10px);
        border-radius: 14px;
        padding: 15px;
        border: 1px solid rgba(255,255,255,0.15);
    }}

    .user-msg {{
        background: rgba(37,99,235,0.85);
        color: white;
        padding: 12px;
        border-radius: 10px;
        margin: 10px 0;
    }}

    .assistant-msg {{
        background: rgba(34,197,94,0.85);
        color: white;
        padding: 12px;
        border-radius: 10px;
        margin: 10px 0;
    }}

    .source-chunk {{
        background: rgba(15,23,42,0.7);
        color: white;
        border-radius: 8px;
        padding: 10px;
        margin: 5px 0;
    }}

    .stButton > button {{
        border-radius: 10px;
    }}

    #MainMenu {{
        visibility: hidden;
    }}

    footer {{
        visibility: hidden;
    }}

    header {{
        visibility: hidden;
    }}

    </style>
    """,
    unsafe_allow_html=True
)

# Session State
if "rag" not in st.session_state:
    st.session_state.rag = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "docs_loaded" not in st.session_state:
    st.session_state.docs_loaded = False
if "num_chunks" not in st.session_state:
    st.session_state.num_chunks = 0

# Sidebar
with st.sidebar:
    st.markdown("## 🎓 College Assistant")
    st.markdown("---")

    st.markdown("### 📄 Upload College Documents")
    st.caption("Syllabi, Notices, Rules, Study Material — any PDF or TXT")

    uploaded_files = st.file_uploader(
        "Drop files here",
        type=["pdf", "txt"],
        accept_multiple_files=True,
        label_visibility="collapsed"
    )

    st.markdown("### ⚙️ Chunking Settings")
    chunk_size = st.slider(
        "Chunk Size (characters per piece)",
        min_value=200, max_value=1000, value=500, step=50,
        help="How many characters per text chunk."
    )
    chunk_overlap = st.slider(
        "Chunk Overlap",
        min_value=0, max_value=200, value=50, step=10,
        help="Characters overlap between chunks."
    )

    st.markdown("---")

    if st.button("🚀 Build Knowledge Base", type="primary", use_container_width=True):
        if not uploaded_files:
            st.error("❌ Please upload at least one document.")
        else:
            with st.spinner("🔄 Processing documents..."):
                try:
                    temp_dir = Path("temp_docs")
                    temp_dir.mkdir(exist_ok=True)
                    file_paths = []

                    for f in uploaded_files:
                        path = temp_dir / f.name
                        path.write_bytes(f.read())
                        file_paths.append(str(path))

                    rag = RAGPipeline(
                        chunk_size=chunk_size,
                        chunk_overlap=chunk_overlap
                    )
                    num_chunks = rag.build_index(file_paths)

                    st.session_state.rag = rag
                    st.session_state.docs_loaded = True
                    st.session_state.num_chunks = num_chunks

                    st.success(f"✅ Indexed {num_chunks} chunks from {len(uploaded_files)} file(s)!")

                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

    if st.session_state.docs_loaded:
        st.markdown("---")
        st.markdown("### 📊 Index Status")
        col1, col2 = st.columns(2)
        col1.metric("📦 Chunks", st.session_state.num_chunks)
        col2.metric("📄 Files", len(uploaded_files) if uploaded_files else "–")

    st.markdown("---")
    st.markdown("### ℹ️ How RAG Works")
    with st.expander("Click to understand the pipeline"):
        st.markdown("""
**Step 1 — Load** 📥  Read your PDFs and extract all text.

**Step 2 — Chunk** ✂️  Break long text into small overlapping pieces (~500 chars each).

**Step 3 — Embed** 🔢  Convert each chunk into a list of numbers (a "vector") that captures its meaning.

**Step 4 — Store** 💾  Save all vectors into FAISS (a super-fast search engine).

**Step 5 — Query** ❓  Your question is converted to a vector, FAISS finds similar chunks, chunks + question are sent to Gemini, which returns a grounded answer.
        """)

# Main Area
st.markdown("# 🎓 College Document Assistant")
st.markdown("*Ask anything about your uploaded college documents — *")

if not st.session_state.docs_loaded:
    st.info("👈 Upload your college documents and click **Build Knowledge Base** to get started.")

    st.markdown("---")
    st.markdown("## 🔍 How this RAG Pipeline Works")

    cols = st.columns(5)
    steps = [
        ("📥", "1. Load",   "Read PDFs/TXT files and extract raw text"),
        ("✂️", "2. Chunk",  "Split text into 500-char overlapping pieces"),
        ("🔢", "3. Embed",  "Convert chunks to vectors using HuggingFace"),
        ("💾", "4. Index",  "Store vectors in FAISS vector database"),
        ("🤖", "5. Answer", "Retrieve + send to Gemini for smart answers"),
    ]
    for col, (icon, title, desc) in zip(cols, steps):
        with col:
            st.markdown(f"""
<div class="metric-card">
  <div style="font-size:2rem">{icon}</div>
  <div style="color:#60a5fa;font-weight:600;margin:8px 0">{title}</div>
  <div style="font-size:0.8rem;color:#94a3b8">{desc}</div>
</div>
""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("## 💡 Example Questions You Can Ask")
    for q in [
        "What is the exam schedule for this semester?",
        "What are the library rules and timings?",
        "Summarize the syllabus for Data Structures.",
        "What are the hostel rules?",
        "List all important dates mentioned in the documents.",
    ]:
        st.markdown(f"- 🔵 *{q}*")

else:
    st.markdown("---")

    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f'''<div class="user-msg">👤 <b>You:</b> {msg["content"]}</div>''',
                        unsafe_allow_html=True)
        else:
            st.markdown(f'''<div class="assistant-msg">🤖 <b>Assistant:</b><br>{msg["content"]}</div>''',
                        unsafe_allow_html=True)
            if "sources" in msg and msg["sources"]:
                with st.expander(f"📎 View {len(msg['sources'])} source chunk(s) used"):
                    for i, src in enumerate(msg["sources"], 1):
                        st.markdown(f'''<div class="source-chunk"><b>Chunk {i}:</b> {src}</div>''',
                                    unsafe_allow_html=True)

    col1, col2 = st.columns([5, 1])
    with col1:
        question = st.text_input(
            "Ask a question",
            placeholder="e.g. What is the exam date for Computer Networks?",
            label_visibility="collapsed",
            key="question_input"
        )
    with col2:
        send = st.button("Ask →", type="primary", use_container_width=True)

    st.markdown("**Quick questions:**")
    q_cols = st.columns(3)
    sample_qs = [
        "Summarize the main topics covered",
        "What are the important rules?",
        "List all key dates mentioned",
    ]
    for i, (qcol, sq) in enumerate(zip(q_cols, sample_qs)):
        if qcol.button(sq, key=f"sample_{i}"):
            question = sq
            send = True

    if send and question:
        st.session_state.chat_history.append({"role": "user", "content": question})

        with st.spinner("🔍 Searching documents and thinking..."):
            try:
                answer, sources = st.session_state.rag.query(question)
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": answer,
                    "sources": sources
                })
            except Exception as e:
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": f"❌ Error: {str(e)}",
                    "sources": []
                })

        st.rerun()

    if st.session_state.chat_history:
        if st.button("🗑️ Clear Chat"):
            st.session_state.chat_history = []
            st.rerun()