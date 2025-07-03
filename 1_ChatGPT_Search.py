import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.agents import load_tools, initialize_agent

# Streamlit app
st.title('LangChain Search')

# Get OpenAI API key, SERP API key and search query
openai_api_key = st.text_input("OpenAI API Key", type="password")
serpapi_api_key = st.text_input("SERP API Key", type="password")
search_query = st.text_input("Search Query")

# Check if the 'Search' button is clicked
if st.button("Search"):
    # Validate inputs
    if not openai_api_key.strip() or not serpapi_api_key.strip() or not search_query.strip():
        st.write(f"Please provide the missing fields.")
    else:
        try:
            # Initialize the OpenAI module, load the SerpApi tool, and run the search query using an agent
            llm=ChatOpenAI(temperature=0, openai_api_key=openai_api_key, verbose=True, model_name = 'gpt-4o-mini')
            tools = load_tools(["serpapi"], llm, serpapi_api_key=serpapi_api_key)
            agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True, handle_parsing_errors=True)

            result = agent.run(search_query)

            st.write(result)
        except Exception as e:
            st.write(f"An error occurred: {e}")