import sys
import pyttsx3
import json
import requests
import pywhatkit
import wikipedia
import yagmail
import time
import speech_recognition as sp
from time import sleep
from urllib.request import urlopen
from playsound import playsound
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal, QThreadPool, QRunnable
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine

# Initializing a variable to store the current state and the result
currentState = None
result = ""

app = QGuiApplication(sys.argv)
# The QQmlApplicationEngine allows using the Qml file as UI layer instead of QtWidgets
engine = QQmlApplicationEngine()

# Now, we connect the app's quit function with the UI layer's quit functions,
# so when we quit the ui, the app also closes
engine.quit.connect(app.quit)
# Loading the Qml file for the UI
engine.load('./UI/main.qml')

# Creating references to the UI elements
win = engine.rootObjects()[0]
startButton = win.findChild(QObject, "startButton")
centerText = win.findChild(QObject, "center")
topText = win.findChild(QObject, "top")
bottomText = win.findChild(QObject, "bottom")
idleAnimation = win.findChild(QObject, "idleAnimation")
processAnimation = win.findChild(QObject, "processAnimation")

pool = QThreadPool.globalInstance()

tts = pyttsx3.init()
sound = tts.getProperty('voices')
tts.setProperty('voice', sound[1].id)
tts.startLoop(False)


class Backend(QObject):
    def __init__(self):
        QObject.__init__(self)

    center = pyqtSignal(str, arguments=['center_label'])
    top = pyqtSignal(str, arguments=['top_label'])
    bottom = pyqtSignal(str, arguments=['bottom_label'])

    def center_label(self, msg):
        self.center.emit(msg)

    def top_label(self, msg):
        self.top.emit(msg)

    def bottom_label(self, msg):
        self.bottom.emit(msg)


class Email:
    # class to create email object
    def __init__(self):
        self.contacts = {'ALVEENA': 'ahmedalveena0125@gmail.com'}
        self.message = ""
        self.email_flag = False
        self.receiver = ""

    # Setters and getters
    def add_contact(self, contact_name, contact_mail):
        self.contacts[contact_name] = contact_mail

    def get_contacts(self):
        return self.contacts

    def set_message(self, message):
        self.message = message

    def set_receiver(self, receiver):
        self.receiver = receiver

    def set_flag(self):
        self.email_flag = True

    def unset_flag(self):
        self.email_flag = False

    def get_receiver(self):
        return self.receiver

    def get_message(self):
        return self.message

    def get_flag(self):
        return self.email_flag

    def send_mail(self, receiver, message):
        # method to send email
        sender = yagmail.SMTP('ahmedalveena0125@gmail.com', 'Alveena0125')
        sender.send(to=receiver, subject='This is an automated mail', contents=message)


class Lights:
    # Class to create lights objects
    def __init__(self):
        self.light_status = False

    # method to switch ON lights
    def switch_on(self):
        self.light_status = True

    # method to switch OFF lights
    def switch_off(self):
        self.light_status = False

    # method to get lights status
    def get_status(self):
        return self.light_status


back_end = Backend()
light = Lights()
email = Email()


def decode_speech_google(source):
    # Using Google web speech to convert speech to text
    rec = sp.Recognizer()
    print("I am listening!")

    try:
        rec.adjust_for_ambient_noise(source)  # adjusting for noise
        audio = rec.listen(source)  # listening to mic
        detected = rec.recognize_google(audio)  # retrieving the detected text from speech
        print(detected)
        # converting detected string into a list of words
        # returning the list
        return detected
    except:
        # if some error occurs then return the word 'error'
        print("An exception occurred")
        return "error"


def search_command(transcript):
    global result
    # Function to search for commands inside the text converted from speech
    command_found = False  # flag to check if any command is found or not
    command_detected = ""
    all_commands = ['WIKIPEDIA', 'LIGHTS', 'WEATHER', 'ACTIVITY', 'PLAY', 'EMAIL', 'TIME', 'CHROME', 'GOOGLE']  # List of commands
    for command in all_commands:  # Searching for all the commands through a loop
        if command in transcript:
            print('command found:', command)  # if command is found print 'command found'
            command_found = True  # Set flag to true if command is found
            command_detected = command
            break  # break the loop as command has been found

    # We need to call relevant function based on command found
    if command_found:
        if command_detected == 'LIGHTS':
            lights_task(transcript)  # Call function to switch on or off the lights
        elif command_detected == 'WEATHER':
            weather()  # Call function to get weather updates
        elif command_detected == 'ACTIVITY':
            activity()  # Call function to get activity suggestion
        elif command_detected == 'WIKIPEDIA':
            search_wiki(transcript)  # Call function to search information on Wikipedia
        elif command_detected == 'PLAY':
            play_song(transcript)
        elif command_detected == 'EMAIL':
            ask_message(transcript)
        elif command_detected == 'TIME':
            tell_time()
        elif command_detected == 'CHROME':
            open_chrome()
        elif command_detected == 'GOOGLE':
            search(transcript)
        else:
            result = "I don't know that"
            currentState.next()
            print("I don't know that")  # if no match found, default action
    else:
        result = "I don't know that"
        currentState.next()
        print("I don't know that")  # if no command found, default action


def lights_task(transcript):
    global result
    # Function to switch on or off lights based on command
    # If command ON is found in text then turn ON the lights
    if "ON" in transcript:
        # getting status by calling get status method from lights class
        if light.get_status():
            result = "Lights are already ON"
            # speak('Lights are already ON')
        else:
            light.switch_on()  # calling switch ON method from lights class
            result = "Lights have been turned ON"
            # speak('Lights have been turned ON')
    elif "OFF" in transcript:  # If command OFF is found in text then turn OFF lights
        light.switch_off()  # calling switch OFF method from lights class
        result = "Lights have been turned OFF"
        # speak('Lights have been turned OFF')
    else:  # Default action if ON or OFF couldn't be detected
        if light.get_status():
            result = "Lights are currently ON"
            # speak('Lights are currently ON ')
        else:
            result = "Lights are currently OFF"
            # speak('Lights are currently OFF')
    currentState.next()


def list_to_string(list_to_convert):
    result_str = ""
    for element in list_to_convert:
        result_str += element+" "
    return result_str


def search(query):
    print(query)
    google_index = query.index('GOOGLE')
    final_query = list_to_string(query[google_index+1:])
    speak("Searching")
    driver = webdriver.Chrome(executable_path="C:\Program Files (x86)\chromedriver.exe")
    global result
    result = "Showing your result on Chrome"
    currentState.next()
    driver.get("https://www.google.com/")
    search_engine = driver.find_element_by_name("q")
    search_engine.send_keys(final_query + Keys.ENTER)


def open_chrome():
    speak("opening chrome")
    driver = webdriver.Chrome(executable_path="C:\Program Files (x86)\chromedriver.exe")
    global result
    result = "Opening Chrome"
    currentState.next()
    driver.get("https://www.google.com/")


def tell_time():
    localtime = time.asctime(time.localtime(time.time()))
    a = localtime[11:16]
    global result
    result = "Your current local time is "+a
    currentState.next()
    # speak(a)


def weather():
    city = get_city()
    get_weather(city)


def get_city():
    # opening the URL to get location
    with urlopen("https://geolocation-db.com/jsonp/IP") as url:
        # reading and decoding the URL and storing to Location
        location = url.read().decode()
        # splitting string with and removing " characters
        location = location.split("(")[1].strip(")")
        # converting json to python
        location = json.loads(location)
        print(location['city'])
    return location['city']


# creating weather function
def get_weather(city_name):
    if city_name is not None:
        # getting data from the URL
        r = requests.get(
            'http://api.openweathermap.org/data/2.5/weather?q=' + city_name + '&APPID=2c0d8e2ba31d6901869ef9e61f9b57cf')
        # using the content of the request
        a = r.json()
        weather_report = ''
        weather_report += ('Current Temperature is ' + str(round(float(a['main']['temp']) - 273.15, 3))+' degree celsius ')
        weather_report += ('It feels like '+ str(round(float(a['main']['feels_like']) - 273.15, 3))+' degree celsius ')
        weather_report += ('Minimum Temperature is ' + str(round(float(a['main']['temp_min']) - 273.15, 3))+ ' degree celsius ')
        weather_report += ('Maximum Temperature is ' + str(round(float(a['main']['temp_max']) - 273.15, 3)) + ' degree celsius ')
        print(weather_report)
        global result
        result = weather_report
        # speak(weather_report)
    else:
        result = "I was not able to fetch your city data"
    currentState.next()


def activity():
    # Function to connect to an API which suggests an activity
    act = requests.get("https://www.boredapi.com/api/activity/")
    act = act.json()
    print(act['activity'])
    # speak(act['activity'])
    global result
    result = "You can "+act['activity']
    currentState.next()


def play_song(transcript):
    # Function to play video on youtube
    try:
        song = ' '.join(map(str, transcript))
        # Replacing extra words
        song = song.replace('ASSISTANT', '')
        song = song.replace('PLAY', '')
        print('playing ', song)
        # speak('playing ' + song)
        global result
        result = "playing "+song
        pywhatkit.playonyt(song)
    except:
        result = "I could not find your requested song"
        print('Could not find your request')
    currentState.next()


def search_wiki(transcript):
    # pip install wikipedia
    # creating a sentence from the list of detected words
    search_string = ' '.join(map(str, transcript))
    # Words to be removed from string before sending for wikipedia search
    extra_word = ['ASSISTANT ', ' SEARCH ', ' ASK ', ' WIKIPEDIA ', ' FOR ', ' ABOUT ']
    for word in extra_word:
        # replacing extra words by blanks
        search_string = search_string.replace(word, ' ')
    print(search_string)
    # getting results from wikipedia API
    try:
        wiki_result = wikipedia.summary(search_string, sentences=1)
        # speaking the results
        global result
        result = wiki_result
        # speak(wiki_result)
    except wikipedia.DisambiguationError as e:
        options = e.options[0:5]
        result = "Please be more specific about what you want to search. I got many results like"
        # speak('Please be more specific about what you want to search. I got many results like')
        # speak(' '.join(map(str, options)))
    except:
        result = "Sorry, I could not fetch results for your query"
    currentState.next()


def ask_message(transcript):
    # function to ask user for message
    search_string = ' '.join(map(str, transcript))
    # removing extra words
    email.receiver = search_string.rstrip().replace('ASSISTANT SEND EMAIL TO ', '')
    print(email.receiver)
    speak('What message would you like to send')
    # Setting email flag to true indicating there is an email to send
    email.email_flag = True
    currentState.run()


def send_email():
    # function to send email
    contacts = email.get_contacts()
    contact = email.get_receiver()
    message = email.get_message()
    # Checking existence of contact in contact list
    if contact in contacts:
        # getting email id from contact name
        receiver = contacts[contact]
        email.send_mail(receiver, message)
        # speak('Your message has been sent')
        global result
        result = "Your message has been sent"
    else:
        result = "Contact does not exist in your contact list"
        # speak('Contact does not exist in your contact list')
    # Unsetting the email details
    email.unset_flag()
    email.set_receiver('')
    email.set_message('')
    currentState.next()


def speak(msg):
    tts.setProperty('rate', 155)
    tts.say(msg)
    tts.iterate()
    while tts.isBusy():
        sleep(0.05)


class State(QObject):
    def __init__(self):
        QObject.__init__(self)

    def enter(self):
        pass

    def run(self):
        pass

    @pyqtSlot()
    def next(self):
        pass


class SleepState(State):

    def enter(self):
        print("Entering the sleep state")
        self.run()

    def run(self):
        startButton.clicked.connect(self.next)

    def next(self):
        startButton.setProperty("stateVisible", False)
        print("Moving to the Awake State")
        global currentState
        currentState = None
        currentState = AwakeState()
        currentState.enter()


class AwakeState(State):

    def enter(self):
        print("Entering Awake state")
        centerText.setProperty("stateVisible", True)
        self.run()

    def run(self):
        print("running awake state")
        runnable = ShowIntroMessages(self.next)
        pool.start(runnable)

    def next(self):
        centerText.setProperty("stateVisible",False)
        print("Moving to wake word listening state")
        global currentState
        currentState = None
        currentState = WakeWordListenState()
        currentState.enter()


class ShowIntroMessages(QRunnable):
    def __init__(self, cb):
        super().__init__()
        self.cb = cb

    def run(self):
        sleep(0.3)
        back_end.center_label("Hi!")
        tts.setProperty('rate', 126)
        tts.say("Hi")
        tts.iterate()
        while tts.isBusy():
            sleep(0.05)
        tts.setProperty('rate', 155)
        back_end.center_label("I'm Jada, your personal digital assistant")
        tts.say("I'm Jada, your personal digital assistant")
        tts.iterate()
        while tts.isBusy():
            sleep(0.05)
        back_end.center_label("")
        self.cb()


class WakeWordListenState(State):
    def enter(self):
        print("Entering wake work listening state")
        runnable = WakeWordStateIntro(self.run)
        pool.start(runnable)

    def run(self):
        print("running wake word listen state")
        with sp.Microphone() as source:
            while isinstance(currentState, WakeWordListenState):
                print("listening for wake word")
                detected = decode_speech_google(source)
                transcript = detected.strip().upper().split()
                if transcript != 'error':
                    if transcript is not None and transcript[0] == 'ASSISTANT':
                        print('Wake word detected')
                        self.next()

    def next(self):
        print("Moving to command listen state")
        back_end.bottom_label("")
        idleAnimation.setProperty("stateVisible", False)
        global currentState
        currentState = None
        currentState = CommandListenState()
        currentState.enter()


class WakeWordStateIntro(QRunnable):
    def __init__(self, cb):
        super().__init__()
        self.cb = cb

    def run(self):
        sleep(0.5)
        topText.setProperty("stateVisible", True)
        bottomText.setProperty("stateVisible", True)
        sleep(0.5)
        back_end.top_label("How may I help you?")
        tts.setProperty('rate', 155)
        tts.say("How may I help you")
        tts.iterate()
        while tts.isBusy():
            sleep(0.5)
        back_end.bottom_label("Say the wake word 'Jada' to begin")
        idleAnimation.setProperty("stateVisible", True)
        self.cb()


class CommandListenState(State):
    def enter(self):
        runnable = CommandStateIntro(self.run)
        pool.start(runnable)

    def run(self):
        print("running command listen state")
        runnable = CommandProcess()
        pool.start(runnable)

    def next(self):
        runnable = CommandNext()
        pool.start(runnable)


class CommandStateIntro(QRunnable):
    def __init__(self, cb):
        super().__init__()
        self.cb = cb

    def run(self):
        sleep(0.25)
        playsound("./Sounds/start.mp3")
        back_end.top_label("Listening...")
        processAnimation.setProperty("stateVisible", True)
        self.cb()


class CommandProcess(QRunnable):
    def run(self):
        with sp.Microphone() as source:
            while isinstance(currentState, CommandListenState):
                print("listening for command")
                detected = decode_speech_google(source)
                transcript = detected.strip().upper().split()
                back_end.top_label("Processing...")
                back_end.bottom_label(detected)
                if transcript != 'error' and transcript is not None:
                    sleep(2)
                    if email.get_flag():
                        email.set_message(transcript)
                        send_email()
                    else:
                        search_command(transcript)
                    break


class CommandNext(QRunnable):
    def run(self):
        back_end.top_label("")
        back_end.bottom_label("")
        sleep(0.25)
        topText.setProperty("stateVisible", False)
        bottomText.setProperty("stateVisible", False)
        processAnimation.setProperty("stateVisible", False)
        playsound("./Sounds/finish.mp3")
        global currentState
        currentState = None
        currentState = ResultState()
        currentState.enter()


class ResultState(State):
    def enter(self):
        runnable = ResultStateIntro(self.run)
        pool.start(runnable)

    def run(self):
        back_end.center_label(result)
        tts.setProperty('rate', 155)
        tts.say(result)
        tts.iterate()
        while tts.isBusy():
            sleep(0.5)
        self.next()

    def next(self):
        back_end.center_label("")
        global result
        result = ""
        centerText.setProperty("stateVisible", False)
        global currentState
        currentState = None
        currentState = WakeWordListenState()
        currentState.enter()


class ResultStateIntro(QRunnable):
    def __init__(self, cb):
        super().__init__()
        self.cb = cb

    def run(self):
        sleep(0.5)
        centerText.setProperty("stateVisible", True)
        sleep(0.5)
        self.cb()


if __name__ == '__main__':
    engine.rootObjects()[0].setProperty("backend", back_end)
    currentState = SleepState()
    currentState.enter()

sys.exit(app.exec())
