import streamlit as st
from chains import ask_pdf, generate_summary, extract_keypoints

st.set_page_config(
    page_title="Large PDF Analyzer",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Large PDF Analyzer")

# Create tabs for different functionalities
tab1, tab2, tab3 = st.tabs(["Ask Questions", "Summary", "Key Points"])

# Tab 1: Ask Questions
with tab1:
    st.header("Ask a Question About Your PDF")
    
    question = st.text_input(
        "Enter your question:",
        placeholder="What is this document about?"
    )
    
    if question:
        with st.spinner("Analyzing your question..."):
            answer = ask_pdf(question)
            st.write(answer)

# Tab 2: Generate Summary
with tab2:
    st.header("PDF Summary")
    
    if st.button("Generate Summary", key="summary_btn"):
        with st.spinner("Generating summary..."):
            summary = generate_summary()
            st.write(summary)

# Tab 3: Extract Key Points
with tab3:
    st.header("Extract Key Points")
    
    if st.button("Extract Key Points", key="keypoints_btn"):
        with st.spinner("Extracting key points..."):
            keypoints = extract_keypoints()
            st.write(keypoints)