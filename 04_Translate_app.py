##### 기본 정보 불러오기 ####
# Streamlit 패키지 추가
import streamlit as st
# OpenAI 패키지 추가
import openai
# 구글 번역 패키지 추가
from googletrans import Translator
# Deepl 번역 패키지 추가
import deepl
# 파파고 API요청을 위한 Requests 패키지 추가 
import requests

##### 기능 구현 함수 #####
# ChatGPT 번역
def gpt_translate(messages):
    messages_prompt = [{"role": "system", "content": f'Translate the following english text into Korean. Text to translate : {messages}'}]
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages_prompt)

    system_message = response["choices"][0]["message"]

    return system_message["content"]

# 파파고 번역
def papago_translate(text,PAPAGO_KEYID,PAPAGO_KEY):
    data = {'text' : text,
            'source' : 'en',
            'target': 'ko'}

    url = "https://openapi.naver.com/v1/papago/n2mt"

    url = "https://naveropenapi.apigw.ntruss.com/nmt/v1/translation"
    header = {"X-NCP-APIGW-API-KEY-ID":PAPAGO_KEYID,
              "X-NCP-APIGW-API-KEY":PAPAGO_KEY,
              "Content-Type":"application/x-www-form-urlencoded" }

    response = requests.post(url, headers=header, data=data)
    rescode = response.status_code

    if(rescode==200):
        send_data = response.json()
        trans_data = (send_data['message']['result']['translatedText'])
        return trans_data
    else:
        print("Error Code:" , rescode)

# 구글 번역
def google_trans(messages):
    google = Translator()
    result = google.translate(messages, dest="ko")

    return result.text

# 디플 번역
def deepl_translate(text, deeplAPI):
    translator = deepl.Translator(deeplAPI)
    result = translator.translate_text(text, target_lang="KO")
    return result.text

##### 메인 함수 #####
def main():
    # 기본 설정
    st.set_page_config(
        page_title="번역 플랫폼 모음",
        layout="wide")

    # session state 초기화
    if "OPENAI_API" not in st.session_state:
        st.session_state["OPENAI_API"] = ""

    if "PAPAGO_KEYID" not in st.session_state:
        st.session_state["PAPAGO_KEYID"] = ""

    if "PAPAGO_KEY" not in st.session_state:
        st.session_state["PAPAGO_KEY"] = ""

    if "DeeplAPI" not in st.session_state:
        st.session_state["DeeplAPI"] = ""


    # 사이드바 바 생성
    with st.sidebar:

        # Open AI API 키 입력받기
        st.session_state["OPENAI_API"] = st.text_input(label='OPENAI API 키', placeholder='Enter Your OpenAI API Key', value='',type='password')

        st.markdown('---')

        # PAPAGO API ID/PW 입력받기
        st.session_state["PAPAGO_KEYID"] = st.text_input(label='PAPAGO API KEYID', placeholder='Enter PAPAGO KEYID', value='')
        st.session_state["PAPAGO_KEY"] = st.text_input(label='PAPAGO API KEY', placeholder='Enter PAPAGO KEY', value='',type='password')

        st.markdown('---')

        # PAPAGO API ID/PW 입력받기
        st.session_state["DeeplAPI"] = st.text_input(label='Deepl API 키', placeholder='Enter Your Deepl API API Key', value='',type='password')
    
        st.markdown('---')

    # 제목 
    st.header('번역 플랫폼 비교하기 프로그램')
    # 구분선
    st.markdown('---')
    st.subheader("번역을 하고자 하는 텍스트를 입력하세요")
    txt = st.text_area(label="",placeholder="input English..", height=200)
    st.markdown('---')

    st.subheader("ChatGPT 번역 결과")
    st.text("https://openai.com/blog/chatgpt")
    if st.session_state["OPENAI_API"] and txt:
        openai.api_key = st.session_state["OPENAI_API"]
        result = gpt_translate(txt)
        st.info(result)
    else:
        st.info('API 키를 넣으세요')
    st.markdown('---')

    st.subheader("파파고 번역 결과")
    st.text("https://papago.naver.com/")
    if st.session_state["PAPAGO_KEYID"] and st.session_state["PAPAGO_KEY"] and txt:
        result = papago_translate(txt,st.session_state["PAPAGO_KEYID"],st.session_state["PAPAGO_KEY"])
        st.info(result)
    else:
        st.info('파파고 KEYID, KEY를 넣으세요')
    st.markdown('---')

    st.subheader("Deepl 번역 결과")
    st.text("https://www.deepl.com/translator")
    if st.session_state["DeeplAPI"] and txt:
        result = deepl_translate(txt,st.session_state["DeeplAPI"])
        st.info(result)
    else:
        st.info('API 키를 넣으세요')

    st.subheader("구글 번역 결과")
    st.text("https://translate.google.co.kr/")
    if txt:
        result = google_trans(txt)
        st.info(result)
    else:
        st.info("API키가 필요 없습니다")
    st.markdown('---')

if __name__=="__main__":
    main()
