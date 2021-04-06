# -*- coding: utf-8 -*-
"""Labeling

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/181PZvSqn3B43ztINEO_ItZKnGi2N3VaO
"""

import pandas as pd
import re

print("Define Func : labeling(file_path)")

def show_text(text):
    
    oneline_words = 20
    
    text = text.replace("." , "")
    text = text.replace("," , "")
    text = text.replace("\n" , " ")
    text = re.split(r'[?]', text)
                      
    for i,t in enumerate(text):
        if len(t) < oneline_words and i + 1 < len(text) and len(text[i+1]) + len(t) < oneline_words:
            print(text[i] + text[i + 1])
        else:
            print(t)

def labeling(file_path):

  # 데이터 로드
  data = pd.read_csv(file_path)
  data.info()

  # 처음 라벨링하는 경우 초기화 , 아니면 현재 라벨링 상태를 보여줌
  try : 
    print(data['라벨'].value_counts())
  except:
      print("label 칼럼 생성")
      data["라벨"] = [-1]*len(data)

  # 라벨링 작업 진행
  for i in range(len(data)):

    if data.loc[i , '라벨'] == -1:

      show_text(data.loc[i , '댓글 내용'])
      label = input()
      print(" ")
      print("------------------------- ")
      print(" ")

      if label == "0" or label == "1" or label == "2":
        data.loc[i , '라벨']  = float(label)

      elif label == 'q': break
      elif label == "s": data.to_csv(file_path , index = 'False')
      else:
        print("잘못된 입력입니다 , 다시 입력해주세요")
        i -= 1

  # 자동으로 50개단위로 저장
  if i%50 == 0: data.to_csv(file_path)
    
  # 정상적으로 종료되면 자동저장
  data.to_csv(file_path , index = 'False')