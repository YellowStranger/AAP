# AAP ver 0.2
import speech_recognition as sr
import os
import sys
import webbrowser
import pyttsx3
from datetime import datetime
import subprocess
import g4f
#from langdetect import detect

# Функция для фильтрации текста по языку
#def filter_text(text, language_to_exclude):
   # words = text.split()
   # filtered_words = [word for word in words if detect(word) != language_to_exclude]
   # return ' '.join(filtered_words)

# текст в речь
engine = pyttsx3.init()


# произношениe текста
def talk(text):
    engine.say(text)
    engine.runAndWait()

# log
chat_log = [['SESSION_ID', 'DATE', 'AUTHOR', 'TEXT', 'AUDIO_NUM']]

# Номер сессии
i = 1
while True:
    session_id = str(i)
    if session_id not in os.listdir():
        os.mkdir(session_id)
        break
    else:
        i = i + 1

# Первое сообщение
author = 'Bot'
text = 'Привет, это Пригожин Женя ! Чем я могу вам помочь?'

# Функция записи лога
def log_me(author, text, audio=None):
    now = datetime.now()
    audio_num = ''
    if audio is not None:
        i = 1
        while True:
            audio_num = str(i) + '.wav'
            if audio_num not in os.listdir(session_id):
                with open(os.path.join(session_id, audio_num), "wb") as file:
                    file.write(audio.get_wav_data())
                break
            else:
                i = i + 1
    chat_log.append([session_id, now.strftime("%Y-%m-%d %H:%M:%S"), author, text, audio_num])

# первое сообщения и запись в лог
print("Bot: " + text)
talk(text)
log_me(author, text)

# Настройка микро
def command():
    rec = sr.Recognizer()
    with sr.Microphone() as source:
        print('Bot: ...')
        rec.pause_threshold = 1
        rec.adjust_for_ambient_noise(source, duration=1)
        audio = rec.listen(source)
    try:
        text = rec.recognize_google(audio, language="ru-RU").lower()
        print('Вы:  ' + text[0].upper() + text[1:])
        log_me('User', text, audio)
    except sr.UnknownValueError:
        text = 'Не понимаю. Повторите.'
        print('Bot: ' + text)
        talk(text)
        return None
    return text

def makeSomething(text):
    if text is None:
        return True

    if 'открой поиск' in text or 'открой Яндекс' in text:
        talk('Открываю Яндекс.')
        webbrowser.open('https://ya.ru/')
        log_me('Bot', 'Открываю сайт Яндекс.')
        return False

    elif 'открой Google' in text or 'открой гугл' in text:
        talk('Гугл для слабаков, открываю Яндекс.')
        webbrowser.open('https://ya.ru/')
        return False

    elif 'открой Яху' in text or 'открой Yahoo' in text or 'открой yahoo' in text:
        talk('Яху? Ты вообще кто? открываю Яндекс.')
        webbrowser.open('https://ya.ru/')
        log_me('Bot', 'Открываю сайт Яндекс.')
        return False

    elif 'произнеси' in text or 'скажи' in text or 'повтори' in text:
        talk(text[10:])
        log_me('Bot', text[10:])

    elif 'своё имя' in text or 'как тебя зовут' in text or 'назови себя' in text:
        talk('Меня зовут Bot')
        log_me('Bot', 'Меня зовут Bot')

    elif 'запусти калькулятор' in text or 'открой калькулятор' in text:
        talk('Секунду')
        subprocess.Popen('C:\\Windows\\System32\\calc.exe')
        log_me('Bot', 'Меня зовут Bot')
        return False

    elif 'запусти проводник' in text or 'открой проводник' in text:
        talk('Секунду')
        subprocess.Popen('C:\\Windows\\explorer.exe')
        log_me('Bot', 'Меня зовут Bot')
        return False

    elif 'пока' in text or 'до свидания' in text or 'пошёл нахрен' in text or 'пошёл на хрен' in text:
        talk('До свидания')
        log_me('Bot', 'Конец сессии')
        with open(os.path.join(session_id, session_id + ".txt"), "w") as log_file:
            for row in chat_log:
                log_file.write(' '.join(str(v) for v in row) + '\n')
        return False
    else:
        talk('Идет переход в GPT. Подождите...')

        g4f.debug.logging = False  # Enable debug logging
        g4f.debug.version_check = False  # Disable automatic version checking
        #print(g4f.Provider.Bing.params)  # Print supported args for Bing


        ## Normal response
        response = g4f.ChatCompletion.create(
            model=g4f.models.gpt_4,
            messages=[{"role": "user", "content": text}],
        )
        #talk_text = filter_text(response, 'en')
        print(response)
        talk(response)
    return True

# Основной цикл
running = True
while running:
    command_text = command()
    if command_text is not None:
        running = makeSomething(command_text)
