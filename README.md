이 문서는 Python 가상환경 설정부터 의존성 설치, 그리고 Streamlit 앱 실행 방법까지의 전체 과정을 안내합니다.

---

## 1️⃣ 파이썬 가상환경 만들기 (venv)

```bash
# 1. 가상환경 생성 (venv 폴더가 생성됨)

    # Windows (CMD 또는 PowerShell)
    python -m venv venv

    # macOS / Linux / WSL
    python3 -m venv venv

# 2. 가상환경 활성화 (OS에 따라 다름)

    # Windows (CMD 또는 PowerShell)
    venv\Scripts\activate

    # macOS / Linux / WSL
    source venv/bin/activate

🔄 가상환경을 비활성화하려면: deactivate
```

## 2️⃣ requirements.txt 설치

```bash
# 가상환경이 활성화된 상태에서 아래 명령어 실행
pip install -r requirements.txt
```

## 3️⃣ Streamlit으로 앱 실행하기

```bash
# 아래 명령어로 Streamlit 앱 실행
streamlit run {filename}.py
```

예:
```bash
streamlit run 1_ChatGPT_Search.py
```

>실행 후 브라우저가 자동으로 열리지 않으면, <br>
>터미널에 표시된 로컬 주소를 복사해서 접속하세요.<br>
>보통은 http://localhost:8501 또는 http://127.0.0.1:8501 입니다.