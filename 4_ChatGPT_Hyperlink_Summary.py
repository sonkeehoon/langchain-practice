import validators, streamlit as st
import re
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain.chains.summarize import load_summarize_chain
from langchain_core.prompts import PromptTemplate
from langchain_core.documents import Document
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, VideoUnavailable

# 스트림릿 앱 제목 표시
st.subheader('URL 요약기')

# 사이드바에서 OpenAI API 키와 모델 선택을 입력받음
with st.sidebar:
    openai_api_key = st.text_input("OpenAI API 키", value="", type="password")
    model = st.selectbox("모델 선택", ("gpt-4o-mini", "gpt-4.1"))

# 메인 화면에서 요약할 URL을 입력받음
url = st.text_input("URL 입력", label_visibility="collapsed")

# 유튜브 URL에서 동영상 ID를 추출하는 함수
def get_youtube_video_id(url):
    # 다양한 유튜브 URL 패턴에서 11자리 동영상 ID 추출
    match = re.search(r"(?:v=|youtu\.be/|embed/|live/|shorts/)([\w-]{11})", url)
    if match:
        return match.group(1)
    return None

# 요약하기 버튼이 눌렸을 때 아래 코드 실행
if st.button("요약하기"):
    # 입력값이 모두 채워졌는지 검사
    if not openai_api_key.strip() or not url.strip():
        st.error("OpenAI API 키와 URL을 모두 입력해야 함")
    # URL이 유효한 형식인지 검사
    elif not validators.url(url):
        st.error("올바른 URL을 입력해야 함")
    else:
        data = None  # 로드된 데이터를 저장할 변수
        try:
            with st.spinner("내용 불러오는 중"):
                video_id = get_youtube_video_id(url)
                if video_id:
                    # 유튜브 URL인 경우 자막 데이터를 가져옴
                    try:
                        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['ko', 'en'])
                        # 자막 텍스트를 하나의 문자열로 합침
                        full_text = " ".join([d['text'] for d in transcript])
                        # LangChain 문서 객체 리스트로 변환
                        data = [Document(page_content=full_text)]
                    except Exception:
                        # 자막이 없거나 에러가 날 경우 오류 표시
                        st.error("유튜브 자막이 없거나 오류 발생")
                        st.stop()
                else:
                    # 유튜브가 아니라 일반 웹페이지라면 UnstructuredURLLoader로 본문 추출
                    loader = UnstructuredURLLoader(urls=[url], ssl_verify=False)
                    data = loader.load()

                # 데이터가 비어 있으면 오류 표시 후 종료
                if not data:
                    st.error("내용을 불러올 수 없음")
                    st.stop()

                # LLM 객체 생성 사용자가 고른 모델과 키 사용
                llm = ChatOpenAI(temperature=0, model=model, openai_api_key=openai_api_key)
                # 요약을 위한 프롬프트 템플릿 정의
                prompt = PromptTemplate(template="다음 내용을 250에서 300단어로 요약하세요 {text}", input_variables=["text"])
                # 요약 체인 생성 stuff 타입으로 간단 요약
                chain = load_summarize_chain(llm, chain_type="stuff", prompt=prompt)
                # 요약 실행
                summary = chain.run(data)

                # 요약 결과를 화면에 출력
                st.write(summary)
        except Exception as e:
            # 예외 발생 시 오류 메시지 표시
            st.error(str(e))