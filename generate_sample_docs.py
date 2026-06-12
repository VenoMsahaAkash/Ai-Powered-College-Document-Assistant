"""
generate_sample_docs.py — Create Fake College Documents for Testing
════════════════════════════════════════════════════════════════════

Run this script to generate sample college documents so you can test
the RAG app immediately without needing real college PDFs.

Usage:
    python generate_sample_docs.py

This creates a folder called `sample_docs/` with 3 text files:
  1. exam_schedule.txt     — Exam dates and rooms
  2. college_rules.txt     — Hostel, library, dress code rules
  3. cs_syllabus.txt       — Computer Science syllabus
"""

import os

os.makedirs("sample_docs", exist_ok=True)

# ─── Document 1: Exam Schedule ─────────────────────────────────
exam_schedule = """EXAMINATION SCHEDULE — SEMESTER 5
Rajiv Gandhi College of Engineering and Technology
Academic Year 2024-25

IMPORTANT NOTICE: All examinations are held in Block C, Floor 2.
Students must carry their hall ticket and college ID.

THEORY EXAMINATIONS:
─────────────────────────────────────────────────────────────────
Subject                        Code    Date          Room
─────────────────────────────────────────────────────────────────
Data Structures                CS301   15 Nov 2024   C201
Computer Networks              CS302   18 Nov 2024   C202
Operating Systems              CS303   20 Nov 2024   C201
Database Management Systems    CS304   22 Nov 2024   C203
Design and Analysis of Algo    CS305   25 Nov 2024   C201
Software Engineering           CS306   27 Nov 2024   C202
─────────────────────────────────────────────────────────────────

EXAM TIMINGS:
Morning Session: 9:00 AM to 12:00 PM
Afternoon Session: 2:00 PM to 5:00 PM

All Semester 5 exams are in the morning session.

PRACTICAL EXAMINATIONS:
─────────────────────────────────────────────────────────────────
Data Structures Lab            CS381   2 Dec 2024    Lab 3
Networks Lab                   CS382   4 Dec 2024    Lab 4
DBMS Lab                       CS383   6 Dec 2024    Lab 5
─────────────────────────────────────────────────────────────────

RULES DURING EXAMINATION:
1. No mobile phones or electronic devices allowed inside exam hall.
2. Students must be seated 10 minutes before the exam starts.
3. Late entry not permitted after 30 minutes of exam start.
4. Students must use only blue or black ballpoint pens.
5. Rough work must be done in the answer sheet itself.
6. Malpractice will lead to immediate cancellation of the examination.

For re-valuation queries, contact the Examination Cell:
Email: exam@rgcet.ac.in | Phone: 0431-2575600 | Room: Admin Block 104
"""

# ─── Document 2: College Rules ─────────────────────────────────
college_rules = """STUDENT HANDBOOK — RULES AND REGULATIONS
Rajiv Gandhi College of Engineering and Technology
(Approved by AICTE | Affiliated to Anna University)

═══════════════════════════════════════════════
LIBRARY RULES
═══════════════════════════════════════════════

Library Timings:
  Weekdays:  8:00 AM – 8:00 PM
  Saturday:  9:00 AM – 5:00 PM
  Sunday:    10:00 AM – 2:00 PM

Borrowing Policy:
  • UG Students can borrow 3 books at a time
  • PG Students can borrow 5 books at a time
  • Loan period: 14 days (renewable once)
  • Fine for late return: Rs. 2 per book per day

Rules:
  1. Maintain complete silence inside the library.
  2. Mobile phones must be switched off or kept on silent.
  3. Personal bags must be deposited at the bag counter.
  4. Eating and drinking strictly prohibited.
  5. Refer to 3 newspapers available in reading section.
  6. Photocopying available at Rs. 1 per page (counter near exit).

═══════════════════════════════════════════════
HOSTEL RULES
═══════════════════════════════════════════════

Boys Hostel (Block H1): Warden — Mr. Rajan | Contact: 9442XXXXXX
Girls Hostel (Block H2): Warden — Mrs. Kavitha | Contact: 9443XXXXXX

Timings:
  Out-pass Timings (weekdays):   6:00 PM only with prior permission
  Out-pass Timings (weekends):   6:00 AM to 9:00 PM
  Lights Out:                    11:00 PM

Rules:
  1. Students must register visitors at the hostel office.
  2. No cooking is allowed inside hostel rooms.
  3. Ragging is a punishable offence under the law.
  4. Students found with alcohol or drugs will be expelled.
  5. Room inspection every Monday at 7:00 AM.
  6. Mess timings: Breakfast 7–8 AM, Lunch 12–1 PM, Dinner 7–8 PM.

═══════════════════════════════════════════════
DRESS CODE
═══════════════════════════════════════════════

  • Monday, Wednesday, Friday: College uniform (white shirt/kurta)
  • Tuesday, Thursday: Department-specific colour code
    - CSE: Light blue shirt
    - ECE: Dark blue shirt
    - MECH: Grey shirt
    - CIVIL: Cream shirt
  • Saturday: Formal casuals allowed (no torn jeans, no sleeveless)

═══════════════════════════════════════════════
ATTENDANCE POLICY
═══════════════════════════════════════════════

Minimum attendance required: 75% in each subject.

Consequences of low attendance:
  < 75%: Not allowed to appear in university exams
  < 65%: Detained and must repeat the semester

Medical leave is considered if submitted within 3 days with
a valid medical certificate from a registered doctor.

For attendance queries: attend@rgcet.ac.in | Admin Block Room 102

═══════════════════════════════════════════════
ANTI-RAGGING COMMITTEE
═══════════════════════════════════════════════

Chairperson: Dr. P. Meenakshisundaram (Principal)
Helpline: 1800-180-5522 (Toll Free, 24x7)
All complaints are treated with strict confidentiality.
"""

# ─── Document 3: CS Syllabus ─────────────────────────────────
cs_syllabus = """DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING
Semester 5 — Curriculum and Syllabus (2021 Regulation)
Rajiv Gandhi College of Engineering and Technology

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CS301 — DATA STRUCTURES (4 Credits)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Unit 1: Linear Data Structures
  Topics: Arrays, Stacks, Queues, Circular Queues, Priority Queues.
  Applications: Expression evaluation, Undo operations, CPU scheduling.

Unit 2: Linked Lists
  Topics: Singly linked list, Doubly linked list, Circular linked list.
  Operations: Insert, delete, search, reverse.

Unit 3: Trees
  Topics: Binary Tree, Binary Search Tree (BST), AVL Tree, B-Tree.
  Traversals: Inorder, Preorder, Postorder.
  Height-balanced trees and rotations.

Unit 4: Graphs
  Topics: Graph representation (Adjacency Matrix, List).
  Algorithms: BFS, DFS, Dijkstra's shortest path, Prim's, Kruskal's MST.

Unit 5: Hashing and Sorting
  Topics: Hash functions, Collision handling (chaining, open addressing).
  Sorting algorithms: Bubble, Selection, Insertion, Merge, Quick, Heap Sort.
  Comparison of time complexities: O(n²) vs O(n log n).

Reference Books:
  1. Introduction to Algorithms — Cormen (CLRS)
  2. Data Structures and Algorithm Analysis — Mark A. Weiss

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CS302 — COMPUTER NETWORKS (4 Credits)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Unit 1: Introduction to Computer Networks
  Topics: Types of networks (LAN, WAN, MAN), Network topologies.
  OSI Model: 7 layers and their functions.
  TCP/IP Model: 4 layers, comparison with OSI.

Unit 2: Data Link Layer
  Topics: Error detection (Parity, CRC, Checksum).
  Error correction: Hamming code.
  Protocols: HDLC, PPP, CSMA/CD (Ethernet).

Unit 3: Network Layer
  Topics: IP addressing (IPv4, IPv6), Subnetting, CIDR.
  Routing protocols: RIP, OSPF, BGP.
  ARP, ICMP, DHCP.

Unit 4: Transport Layer
  Topics: TCP (3-way handshake, flow control, congestion control).
  UDP: Features and use cases.
  Ports and sockets.

Unit 5: Application Layer
  Topics: DNS, HTTP/HTTPS, FTP, SMTP, POP3, IMAP.
  Web security basics: SSL/TLS.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CS304 — DATABASE MANAGEMENT SYSTEMS (4 Credits)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Unit 1: Introduction to Databases
  Topics: Database concepts, DBMS vs File System.
  Data models: Hierarchical, Network, Relational.
  ER Diagrams: Entities, attributes, relationships, cardinality.

Unit 2: Relational Model and SQL
  Topics: Relational algebra (Select, Project, Join, Union).
  SQL: DDL (CREATE, ALTER, DROP), DML (SELECT, INSERT, UPDATE, DELETE).
  Joins: Inner, Left, Right, Full Outer, Cross Join.
  Aggregate functions: COUNT, SUM, AVG, MAX, MIN.

Unit 3: Normalisation
  Topics: Functional dependencies, 1NF, 2NF, 3NF, BCNF.
  Decomposition: Lossless join, Dependency preservation.

Unit 4: Transaction Management
  Topics: ACID properties (Atomicity, Consistency, Isolation, Durability).
  Concurrency control: Locking protocols, Deadlock.
  Recovery: Undo/Redo, Checkpointing.

Unit 5: NoSQL Databases
  Topics: Introduction to NoSQL, Types (Document, Key-Value, Column, Graph).
  MongoDB basics: Collections, documents, CRUD operations.
  When to choose SQL vs NoSQL.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
KEY DATES FOR SEMESTER 5
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Internal Assessment Test 1:   5 September 2024
  Internal Assessment Test 2:   10 October 2024
  Model Exam:                   1 November 2024
  University Exams Begin:       15 November 2024
  Results Expected:             January 2025

Project Reviews:
  Phase 1 Review:               30 September 2024
  Phase 2 Review (Final):       15 January 2025

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FACULTY CONTACT DETAILS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Head of Department:       Dr. S. Jayakumar | hod.cse@rgcet.ac.in
Class Advisor (5-CSE-A):  Mrs. T. Priya   | priya.t@rgcet.ac.in
Class Advisor (5-CSE-B):  Mr. K. Sathish  | sathish.k@rgcet.ac.in
"""

# ─── Write files ───────────────────────────────────────────────
files = {
    "sample_docs/exam_schedule.txt": exam_schedule,
    "sample_docs/college_rules.txt": college_rules,
    "sample_docs/cs_syllabus.txt": cs_syllabus,
}

for filepath, content in files.items():
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ Created: {filepath}")

print("\n🎉 Sample documents created in sample_docs/ folder!")
print("Upload these to the Streamlit app to start testing.")
