import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.agents import load_tools, initialize_agent

# Streamlit app
st.title('LangChain Search')

# Get OpenAI API key, SERP API key and search query
openai_api_key = st.text_input("OpenAI API Key", type="password")
serpapi_api_key = st.text_input("SERP API Key", type="password")

# 사용자에게 검색하고 싶은 문장을 입력받기
search_query = st.text_input("Search Query")

# Serach 버튼을 클릭하면 아래 코드 실행
if st.button("Search"):
    # 세 입력값이 하나라도 비어 있지 않은지 확인함
    if not openai_api_key.strip() or not serpapi_api_key.strip() or not search_query.strip():
        st.write(f"Please provide the missing fields.")
    else:
        try:
            # ChatOpenAI 인스턴스를 생성하고 모델명은 gpt-4o-mini로 지정
            llm = ChatOpenAI(temperature=0, openai_api_key=openai_api_key, verbose=True, model_name = 'gpt-4o')
            tools = load_tools(["serpapi"], llm, serpapi_api_key=serpapi_api_key)
            agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True, handle_parsing_errors=True)

            result = agent.run(search_query)

            st.write(result)
        except Exception as e:
            st.write(f"An error occurred: {e}")