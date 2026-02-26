import streamlit as st
import os
from datetime import datetime
from utils.pdf_parser import extract_text
from utils.llm_processor import summarize, extract_findings
from utils.rag_processor import RAGProcessor
from utils.tts_handler import generate_audio
from utils.report_generator import create_report

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(page_title="Paper Summarizer", page_icon="📚")
st.title("LLM-RAG Powered Scientific Paper Summarizer")

# -------------------------------------------------
# SESSION STATE INIT
# -------------------------------------------------
if "chats" not in st.session_state:
    st.session_state.chats = {}

if "current_chat" not in st.session_state:
    st.session_state.current_chat = None

# -------------------------------------------------
# SIDEBAR - CHAT MANAGEMENT
# -------------------------------------------------
st.sidebar.title("💬 Chat History")

if st.sidebar.button("➕ New Chat"):
    chat_name = f"Chat {datetime.now().strftime('%H:%M:%S')}"

    st.session_state.chats[chat_name] = {
        "messages": [],
        "summary": "",
        "findings": "",
        "processed": False,
        "rag": None
    }

    st.session_state.current_chat = chat_name
    st.rerun()

# Display chats
if st.session_state.chats:
    chat_list = list(st.session_state.chats.keys())

    selected_chat = st.sidebar.radio(
        "Select Chat",
        chat_list,
        index=chat_list.index(st.session_state.current_chat)
        if st.session_state.current_chat in chat_list else 0
    )

    st.session_state.current_chat = selected_chat

# -------------------------------------------------
# MAIN
# -------------------------------------------------
if st.session_state.current_chat is None:
    st.info("👈 Create a new chat from sidebar to begin.")
    st.stop()

chat = st.session_state.chats[st.session_state.current_chat]

# -------------------------------------------------
# FILE UPLOAD (Only if not processed)
# -------------------------------------------------
if not chat["processed"]:
    uploaded_file = st.file_uploader(
        "Upload a scientific paper (PDF)",
        type="pdf"
    )

    if uploaded_file is not None:
        with open("temp.pdf", "wb") as f:
            f.write(uploaded_file.getbuffer())

        text, chunks_or_error = extract_text("temp.pdf")
        os.remove("temp.pdf")

        if isinstance(chunks_or_error, str):
            st.error(chunks_or_error)
            st.stop()

        with st.spinner("Processing paper..."):
            try:
                chat["summary"] = summarize(text)
                chat["findings"] = extract_findings(text)

                # Create fresh RAG object per chat
                rag = RAGProcessor()
                rag.embed_text(chunks_or_error)

                chat["rag"] = rag
                chat["processed"] = True

                st.success("✅ Paper processed successfully!")
                st.rerun()

            except Exception as e:
                st.error(f"Processing error: {str(e)}")
                st.stop()

# -------------------------------------------------
# DISPLAY RESULTS
# -------------------------------------------------
if chat["processed"]:

    with st.expander("📄 Summary", expanded=True):
        st.write(chat["summary"])

    with st.expander("🔎 Key Findings", expanded=True):
        st.markdown(chat["findings"])

    rag = chat["rag"]

    # -------------------------------------------------
    # TTS
    # -------------------------------------------------
    if st.button("🔊 Listen to Summary"):
        audio_path = generate_audio(
            chat["summary"] + "\n" + chat["findings"]
        )
        if not audio_path.startswith("Error"):
            st.audio(audio_path)
        else:
            st.error(audio_path)

    # -------------------------------------------------
    # DOWNLOAD REPORT
    # -------------------------------------------------
    report_path = create_report(
        chat["summary"],
        chat["findings"]
    )

    if not report_path.startswith("Error"):
        with open(report_path, "rb") as f:
            st.download_button(
                label="📥 Download Report",
                data=f,
                file_name="paper_report.pdf",
                mime="application/pdf"
            )

    # -------------------------------------------------
    # CHAT SECTION
    # -------------------------------------------------
    st.subheader("💬 Ask About This Paper")

    for msg in chat["messages"]:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    question = st.chat_input("Ask a question about the paper...")

    if question:
        chat["messages"].append({"role": "user", "content": question})

        with st.chat_message("user"):
            st.write(question)

        with st.spinner("Thinking..."):
            try:
                answer = rag.answer_question(question)
            except Exception as e:
                answer = f"Error: {str(e)}"

        chat["messages"].append({"role": "assistant", "content": answer})

        with st.chat_message("assistant"):
            st.write(answer)
