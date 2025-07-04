import os, streamlit as st
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
from langchain_openai import ChatOpenAI
from langchain.chains.summarize import load_summarize_chain

# Streamlit app
st.title('LangChain Text Summarizer')

# Get OpenAI API key and source text input
openai_api_key = st.text_input("OpenAI API Key", type="password")
source_text = st.text_area("Source Text", height=200)

# Check if the 'Summarize' button is clicked
if st.button("Summarize"):
    # Validate inputs
    if not openai_api_key.strip() or not source_text.strip():
        st.write(f"Please complete the missing fields.")
    else:
        try:
            # 입력받은 텍스틀르 문장 단위로 분할함
            text_splitter = CharacterTextSplitter()
            texts = text_splitter.split_text(source_text)

            # 분할된 텍스트 조각을 Document 객체로 변환
            # 예시에서는 최대 세 개의 텍스트 조각만 사용함
            docs = [Document(page_content=t) for t in texts[:3]]

            # ChatOpenAI 인스턴스를 생성하고 모델명은 gpt-4o-mini로 지정
            llm = ChatOpenAI(temperature=0, openai_api_key=openai_api_key, model_name = "gpt-4o-mini")
            
            # 요약 체인 불러오기 map reduce 방식으로 여러 문제를 요약
            chain = load_summarize_chain(llm, chain_type="map_reduce")
            
            # 요약 체인을 실행하여 문서들을 요약함
            summary = chain.run(docs)

            # Display summary
            st.write(summary)
        except Exception as e:
            st.write(f"An error occurred: {e}")