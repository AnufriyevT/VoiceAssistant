import speech_recognition as sr
import pyttsx3
import datetime
from fuzzywuzzy import fuzz
import time
import random

opts = {
    "alias": ('тимур', 'тима', 'тим', 'тимурчик', 'мур'),
    'tbr': ('скажи', 'расскажи', 'покажи', 'подскажи'),
    'cmds': {
        'ctime': ('который час', 'текущее время', 'сейчас времени', 'времени сколько'),
        'anekdot': ('шутку', 'анекдот', 'рассмеши меня')
    }
}


# функции
def speak(what):
    print(what)
    speak_engine.say(what)
    speak_engine.runAndWait()
    speak_engine.stop()


def callback(recognizer, audio):  # слушает
    try:
        voice = recognizer.recognize_google(audio, language="ru-RU").lower()
        print("Распознано: " + voice)

        if voice.startswith(opts["alias"]):
            cmd = voice
            for x in opts['alias']:
                cmd = cmd.replace(x, "").strip()  # Удаляем имя нашего помощника из команды

            for x in opts['tbr']:
                cmd = cmd.replace(x, "").strip()  # Удаляем команды типа скажи, расскажи и тд

            # распознаем и выполняем команду
            cmd = recognize_cmd(cmd)  # вызываем метод для распознавания команды
            execute_cmd(cmd['cmds'])  # метод для выполнения команды
    except sr.UnknownValueError:
        print("Голос не распознан!")
    except sr.RequestError:
        print("Неизвестная ошибка, проверьте интернет!")


def recognize_cmd(cmd):  # распознает команду
    # Используем fuzzywuzzy, для сравнение нечетких команд со всеми командами
    RC = {'cmd': '', 'percent': 0}
    for c, v in opts['cmds'].items():
        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > RC['percent']:
                RC['cmds'] = c
                RC['percent'] = vrt
    return RC


def execute_cmd(cmd):
    if cmd == 'ctime':
        # сказать текущее время
        now = datetime.datetime.now()
        speak("Сейчас " + str(now.hour) + ":" + str(now.minute))

    elif cmd == 'anekdot':
        # рассказать анекдот
        l = ["Колобок повесился",'Русалка села на шпагат']
        speak(l[random.randint(0, len(l) - 1)])

    else:
        print('Команда не распознана, повторите!')


# запуск
r = sr.Recognizer()
m = sr.Microphone(device_index=1)

with m as source:
    r.adjust_for_ambient_noise(source)  #

speak_engine = pyttsx3.init()

speak("Начните говорить")

stop_listening = r.listen_in_background(m, callback)
while True: time.sleep(0.1)  # infinity loop