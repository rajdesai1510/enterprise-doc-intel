import streamlit as st
import requests
import os
from dotenv import load_dotenv

# ---------------- Setup ----------------
load_dotenv()
BACKEND_URL = os.getenv("BACKEND_URL")

st.set_page_config(
    page_title="Enterprise Document Intelligence",
    page_icon="📄",
    layout="wide"
)

# ---------------- Helper Functions ----------------
def login_user(email: str, password: str):
    response = requests.post(
        f"{BACKEND_URL}/auth/login",
        params={
            "email": email,
            "password": password
        },
        timeout=30
    )

    if response.status_code == 200:
        return response.json()["token"]

    st.error(response.text)
    return None




def get_headers():
    return {
        "Authorization": f"Bearer {st.session_state.token}"
    }


# ---------------- Auth Gate ----------------
if "token" not in st.session_state:
    st.title("🔐 Login")

    username = st.text_input("email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        token = login_user(username, password)
        if token:
            st.session_state.token = token
            st.success("Login successful")
            st.rerun()
        else:
            st.error("Invalid username or password")

    st.stop()

# ---------------- Sidebar ----------------
st.sidebar.title("📄 Enterprise RAG")

namespace = st.sidebar.text_input(
    "Namespace (Tenant / Org)",
    value="default-org"
)

if st.sidebar.button("Logout"):
    del st.session_state.token
    st.rerun()

# ---------------- Upload Section ----------------
st.header("📤 Upload Documents")

uploaded_files = st.file_uploader(
    "Upload PDF documents",
    type=["pdf"],
    accept_multiple_files=True
)

if st.button("Upload"):
    if not uploaded_files:
        st.warning("Please upload at least one PDF")
    else:
        with st.spinner("Uploading documents..."):
            for file in uploaded_files:
                response = requests.post(
                    f"{BACKEND_URL}/documents/upload",
                    files={
                        "file": (file.name, file, "application/pdf")
                    },
                    data={
                        "namespace": namespace
                    },
                    headers=get_headers(),
                    timeout=300
                )

                if response.status_code == 200:
                    st.success(f"Uploaded: {file.name}")
                else:
                    st.error(f"Failed: {file.name} → {response.text}")

# ---------------- Chat Section ----------------
st.divider()
st.header("💬 Ask Questions")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

question = st.text_input(
    "Ask a question about your documents",
    placeholder="What is this document about?"
)

if st.button("Ask"):
    if not question.strip():
        st.warning("Please enter a question")
    else:
        with st.spinner("Querying knowledge base..."):
            response = requests.post(
                f"{BACKEND_URL}/query",
                params={
                    "question": question,
                    "namespace": namespace
                },
                headers=get_headers(),
                timeout=120
            )

            if response.status_code == 200:
                data = response.json()

                st.session_state.chat_history.append({
                    "question": question,
                    "answer": data["answer"],
                    "sources": data.get("sources", [])
                })
            else:
                st.error(f"Error: {response.text}")

# ---------------- Chat History ----------------
for chat in reversed(st.session_state.chat_history):
    st.markdown("**You:**")
    st.write(chat["question"])

    st.markdown("**Answer:**")
    st.write(chat["answer"])

    if chat.get("sources"):
        st.markdown("**Sources:**")
        for src in chat["sources"]:
            st.markdown(
                f"- `{src['filename']}` (chunk {src['chunk_index']}, score {round(src['score'], 3)})"
            )

    st.markdown("---")

