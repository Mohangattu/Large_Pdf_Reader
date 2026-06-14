import streamlit as st
from chains import answer_question

st.set_page_config(
    page_title="Large PDF Analyzer",
    page_icon="📚"
)

st.title("📚 Large PDF Analyzer")

question = st.text_input(
    "Ask a question:"
)

if question:

    with st.spinner("Thinking..."):

        answer = answer_question(question)

        st.subheader("Answer")

        st.write(answer)