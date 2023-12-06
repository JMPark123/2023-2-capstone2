# 모델 다운로드, API call을 통한 문장 생성, 파이프라이닝까지 진행된 python 코드 짜기 필요 -> ipynb를 python 코드로 옮기기
# 설치할것들 install하는 과정 필요, 모델 받아오기 필요, API call 필요

# frontend는 서버 코드에서 api 호출을 통해 요청받은 내용을 처리할 수 있도록 틀만 짜기(문장 입력, 문장 출력, 만든 내용 전달)

# 필요한것


from flask import Flask, request, jsonify
from transformers import AutoModel, AutoTokenizer
from sentence_transformers import SentenceTransformer
from flask_cors import CORS
import torch
import numpy as np
import pandas as pd
from numpy import dot
from numpy.linalg import norm
import urllib.request
import os
import openai
import json

# GPT-3.5-turbo api를 호출하는 라이브러리 등 추가되어야 함

app = Flask(__name__) # flask 애플리케이션을 생성하는 데에 사용되는 구문, python에서 직접 실행되는 경우 __main__이 할당됨, app.py 실행을 함으로써 서버가 구동되게 됨
CORS(app)

# 파일에서 API 키를 읽어오는 함수
def load_api_keys():
    with open('api-key.json') as f:
        api_keys = json.load(f)
    return api_keys

# API 키 불러오기
api_keys = load_api_keys()
openai_api_key = api_keys['openai_key']  # json 파일에 저장된 openai api key를 필요한 키 이름으로 가져옵니다.


# Hugging Face에서 업로드한 모델명
uploaded_model_name = "JungminPark/capstone_sbert"  # 내가 업로드한 모델명

# 사용자가 업로드한 모델을 가져오는 함수
def load_uploaded_model():
    model = SentenceTransformer(uploaded_model_name)
    return model


# 전역 변수로 업로드한 모델 받아온 것을 저장
global sbert_model
sbert_model = load_uploaded_model() # 

# 모델이 성공적으로 불러와졌는지 확인
if sbert_model is not None:
    print("모델이 성공적으로 불러와졌습니다.")
else:
    print("모델을 불러오는 데 실패했습니다.")

'''
# custom으로 만든 코사인 유사도 계산 함수
def cos_sim(A, B):
    return dot(A, B)/(norm(A)*norm(B))
'''
# 코사인 유사도를 계산하는 함수를 생성
def calculate_cosine_similarity(sentence1, sentence2):
    # 2개 sentence의 임베딩 벡터를 구해 코사인 유사도 측정에 활용
    embeddings1 = sbert_model.encode([sentence1], convert_to_tensor=True)
    embeddings2 = sbert_model.encode([sentence2], convert_to_tensor=True)
    # custom_cosine_similarity = cos_sim(embeddings1, embeddings2) # 커스텀 함수를 활용한 유사도
    cosine_similarity = torch.nn.functional.cosine_similarity(embeddings1, embeddings2).item() # torch 라이브러리의 함수를 활용한 유사도
    return cosine_similarity

# openai api key 설정(json 파일에서 불러온)
openai.api_key = openai_api_key

# 처음에는 messages로 API를 통해 전달할 내용을 최초 1회 설정해 줌
gpt_model = "gpt-3.5-turbo"
# messages = []
# messages.append({"role":"system", "content": "너는 괄호로 묶인 input sentence와 유사한 의미 및 구조를 가지지만 단어와 구성 등이 다른 새로운 문장을 생성하는 유사 문장 생성기야. 내 말에 대답 형식으로 말할 필요는 없고 input sentence가 주어지면 그와 같은 맥락과 의미의 문장을 생성하기만 하면 돼."})

# /generate 엔드포인트에서의 POST 요청 처리
# 입력받은 문장을 기반으로 GPT API를 호출해서 유사문장을 생성하도록 유도
@app.route('/generate', methods=['POST'])
def generate():
    content = request.json
    sentence = content['sentence'] # frontend로부터 받아온 sentence를 여기에 저장
    
    # 여기서 sentence를 활용해 작업 수행
    messages = []
    messages.append({"role":"system", "content": "너는 괄호로 묶인 input sentence와 유사한 의미 및 구조를 가지지만 단어와 구성 등이 다른 새로운 문장을 생성하는 유사 문장 생성기야. 내 말에 대답 형식으로 말할 필요는 없고 input sentence가 주어지면 그와 같은 맥락과 의미의 문장을 생성하기만 하면 돼."})

    gpt_content = sentence # gpt에 전달할 content(사용자가 입력한 문장) 부분을 gpt_content라는 변수로 만듬
    messages.append({"role": "user", "content":gpt_content})

    completion = openai.ChatCompletion.create(
        model = gpt_model,
        messages = messages
    )

    chat_response = completion.choices[0].message.content # chat_response를 활용해서 계산 진행

    embedding1 = sbert_model.encode(sentence)
    embedding2 = sbert_model.encode(chat_response)

    # custom_score = cos_sim(embedding1, embedding2)
    score = calculate_cosine_similarity(sentence, chat_response)
    count = 1
    upper_threshold = 0.95 # 0.95가 넘는 코사인 유사도를 가지는 문장은 너무 똑같은 문장으로 판단해 필터링
    lower_threshold = 0.6 # 0.6이 안되는 코사인 유사도를 가지는 문장은 너무 유사하지 않은 문장으로 판단해 필터링

    if (((score < lower_threshold) or (score > upper_threshold)) and (count < 5)):
  # 원하는 cosine similarity에 도달하지 못한 경우 문장을 재생성. 문장 생성 횟수가 5회를 넘은 경우 제대로 된 문장을 생성하지 못했다고 파악하고 루프를 종료시킴
        while ((score < lower_threshold) or (score > upper_threshold) or  (count < 5)):
    # 이전의 내용 최대 5회 루프 하도록 함
    # messages 배열 초기화 후 create 과정을 다시 수행하게 함
            messages = []
            messages.append({"role":"system", "content": "너는 input sentence와 유사한 의미 및 구조를 가지지만 단어와 구성 등이 다른 새로운 문장을 생성하는 유사 문장 생성기야. 내 말에 대답 형식으로 말할 필요는 없고 input sentence가 주어지면 최대한 그와 같은 맥락과 의미의 문장을 생성하기만 하면 돼."})
            messages.append({"role":"user", "content": gpt_content})
            completion = openai.ChatCompletion.create(
                model = gpt_model,
                messages = messages,
            )
            chat_response = completion.choices[0].message.content
            embedding1 = sbert_model.encode(gpt_content)
            embedding2 = sbert_model.encode(chat_response)
            print(chat_response)
            # custom_score = cos_sim(embedding1, embedding2)
            score = calculate_cosine_similarity(gpt_content, chat_response)
            print(score)
            count += 1
            if (count == 5 or ((score < upper_threshold) and (score > lower_threshold))):
                break;

    if (count == 5):
        if ((score < upper_threshold) and (score > lower_threshold)):
            print("\n생성한 문장은 다음과 같습니다.")
            print(chat_response)
            print("\n", count, "회 문장을 생성했습니다. ")
            print("\n유사도는 ", score, "점입니다.")
            return jsonify({'message': chat_response,  'score':score})   
        else:
            print("죄송합니다. 정해진 생성횟수인 5회 이내에 양질의 문장 만들기에 실패했습니다. 다시 문장을 입력해 주십시오.")
            return jsonify({'message': "죄송합니다. 정해진 생성횟수인 5회 이내에 양질의 문장 만들기에 실패했습니다. 다시 문장을 입력해 주십시오.",  'score':score})   
    else:
        print("\n생성한 문장은 다음과 같습니다.")
        print(chat_response)
        print("\n", count, "회 문장을 생성했습니다. ")
        print("\n유사도는 ", score, "점입니다.")
        return jsonify({'message': chat_response,  'score':score, 'count':count})        

    # 이 부분에서 만약 양질의 문장이 잘 생성된 경우 chat_response를 프론트에 리턴해 주고, 양질의 문장이 생성되지 않은 경우 생성되지 않았음을 알리는 문장이 리턴되게

    
    # 잘 저장되었음을 반환하는 메시지 or 생성이 잘 되지 않았음을 알려주는 메시지, 상황에 따라 케이스 분리해서 return할 문장을 다르게 설정해 줘야함
    # return jsonify({'message': chat_response,  'score':score})


if __name__ == '__main__':
    app.run(debug=True)


