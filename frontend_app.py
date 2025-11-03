import streamlit as st
import requests
import json

# FastAPI backend URL
BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Multimodal RAG System", layout="centered")

st.title("🧠 Multimodal RAG System")
st.write("Upload a text, PDF, or image file and ask a question about it!")

# -------------------- Upload Section --------------------
uploaded_file = st.file_uploader("📁 Upload a file", type=["txt", "pdf", "png", "jpg", "jpeg"])

if uploaded_file is not None:
    with st.spinner("⏳ Uploading to backend..."):
        files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
        response = requests.post(f"{BACKEND_URL}/upload/file", files=files)
    
    if response.status_code == 200:
        res_data = response.json()
        if res_data["status"] == "success":
            st.success("✅ File uploaded successfully!")
            st.json(res_data["metadata"])
        else:
            st.error(f"❌ Upload failed: {res_data['message']}")
    else:
        st.error("⚠️ Backend error during upload!")

# -------------------- Query Section --------------------
st.subheader("💬 Ask a question about uploaded data")
query = st.text_input("Enter your query")

if st.button("🔍 Search"):
    if not query:
        st.warning("Please enter a question/query.")
    else:
        with st.spinner("🧠 Searching for best answer..."):
            data = {"query": query}
            res = requests.post(f"{BACKEND_URL}/query", data=data)

        if res.status_code == 200:
            res_json = res.json()
            if res_json["status"] == "success":
                st.success("✅ Query successful!")
                st.write("**Top Results:**")
                for item in res_json["results"]:
                    st.markdown(f"📄 **Source:** {item['source']}")
                    st.markdown(f"🔹 **Relevance:** {item['relevance_score']}")
                    st.text(item["content"])
                    st.write("---")
            else:
                st.error(res_json.get("message", "Unknown error"))
        else:
            st.error("⚠️ Backend error during query request!")