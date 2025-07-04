import os, tempfile
import streamlit as st
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.vectorstores.chroma import Chroma
# from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains.summarize import load_summarize_chain
from langchain.document_loaders import PyPDFLoader

# Streamlit app
st.title('LangChain Doc Summarizer')

# Get OpenAI API key and source document input
openai_api_key = st.text_input("OpenAI API Key", type="password")
source_doc = st.file_uploader("Upload Source Document", type="pdf")

# Check if the 'Summarize' button is clicked
if st.button("Summarize"):
    # Validate inputs
    if not openai_api_key.strip() or not source_doc:
        st.write(f"Please provide the missing fields.")
    else:
        try:
            # 업로드된 PDF 파일을 임시 파일로 저장
            with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                tmp_file.write(source_doc.read())
            
            # 임시파일을 PyPDFLoader로 로드하고 페이지단위로 분할함
            loader = PyPDFLoader(tmp_file.name)
            pages = loader.load_and_split()
            
            # 임시로 저장된 파일을 삭제하여 공간을 정리
            os.remove(tmp_file.name)

            # 페이지별로 임베딩 생성, 벡터 DB에 저장
            embeddings=OpenAIEmbeddings(openai_api_key=openai_api_key)
            vectordb = Chroma.from_documents(pages, embeddings)

            # ChatOpenAI 인스턴스를 생성하고 모델명은 gpt-4o-mini로 지정
            llm=ChatOpenAI(temperature=0, openai_api_key=openai_api_key, verbose=True, model_name = 'gpt-4o-mini')
            chain = load_summarize_chain(llm, chain_type="stuff")
            search = vectordb.similarity_search(" ")
            summary = chain.run(input_documents=search, question="Write a summary within 150 words.")

            st.write(summary)
        except Exception as e:
            st.write(f"An error occurred: {e}")