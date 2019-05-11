# -*- coding: utf-8 -*-

from wox import Wox,WoxAPI
import requests
import json
import webbrowser,os
import os,sys
import urllib.request
from playsound import playsound

class HelloWorld(Wox):
    def query(self,key):
        results = []
        location = f'http://fanyi.youdao.com/openapi.do?keyfrom=neverland&key=969918857&type=data&doctype=json&version=1.1&q={key}'
        html = requests.get(location).text
        dicts = json.loads(html)
        html = json.dumps(dicts, sort_keys=True, indent=4, separators=(',', ':'))
        # 获取翻译结果
        translate_result = dicts['translation'][0]
        results.append({"Title": translate_result,"SubTitle":"Translate Result","IcoPath":"Images/translate.ico","JsonRPCAction":{"method": "hide_app","parameters":[],"dontHideAfterAction":True}})
        if('basic' in dicts.keys()):
            basic_meaning = dicts['basic']
            # 获取音标
            if('us-phonetic' in basic_meaning.keys()):
                pronunciation_us = basic_meaning['us-phonetic']
            else:
                pronunciation_us = ''
            if('uk-phonetic' in basic_meaning.keys()):
                pronunciation_uk = basic_meaning['uk-phonetic']
            else:
                pronunciation_uk = ''
            if(pronunciation_us or pronunciation_uk):
                results.append({"Title": '[US]: ['+pronunciation_us+']   [UK]: ['+pronunciation_uk+']',"SubTitle":"Pronunciation","IcoPath":"Images/audio2.ico","JsonRPCAction":{"method": "read_word","parameters":[key],"dontHideAfterAction":True}})
            # 获取单词解释
            meanings = basic_meaning['explains']
            for meaning in meanings:
                title = meaning
                results.append({
                    "Title": title,
                    "SubTitle":"Word Explanations",
                    "IcoPath":"Images/app.ico"
                    })
        return(results)
    def hide_app(self):
        WoxAPI.change_query('d ')
    def read_word(self,word):
        file = self.down_mp3(word)
        playsound(file)
    def down_mp3(self,word):
        word = word.lower()  # 小写
        fileName = word + '.mp3'
        if not os.path.exists('Speech_US'):
            # 不存在，就创建
            os.makedirs('Speech_US')
        dirSpeech = os.path.join(os.path.split( os.path.realpath(sys.argv[0] ) )[0], 'Speech_US')  # 美音库
        filePath = os.path.join(dirSpeech, fileName)

        if os.path.exists(filePath):
            return filePath
        else:
            audio_url = r'http://dict.youdao.com/dictvoice?type=' + '0' + r'&audio=' + word
            music_data = requests.get(audio_url).content
            with open(filePath,'wb') as f:
                f.write(music_data)
            return filePath
if __name__ == "__main__":
    HelloWorld()
