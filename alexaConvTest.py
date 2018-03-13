from flask import Flask, Session
from flask_ask import Ask, question, statement, session

__author__ = 'Laurence Elliott'

app = Flask(__name__)
ask = Ask(app, "/")

@ask.launch
def start_skill():
    welcome_message = '<speak>Welcome to the student wellbeing centre Alexa skill. Would you like to: <prosody volume="x-loud"><emphasis>get advice</emphasis></prosody> on an issue, or, <prosody volume="x-loud"><emphasis>learn more,</emphasis></prosody> about the wellbeing centre.</speak>'
    session.attributes["curNode"] = 0
    session.attributes["prevNode"] = -1
    getNodes()
    return question(welcome_message).simple_card(content=welcome_message)

@ask.session_ended
def session_ended():
    return "{}", 200

@ask.intent("AMAZON.HelpIntent")
def help():
    return question('<speak>You can ask me to stop the skill by saying "stop", "cancel", or "exit".</speak>')


@ask.intent("AMAZON.StopIntent")
def stop():
    return statement("It was nice speaking with you. Goodbye.")


@ask.intent("GetAdvice")
def getAdvice():
    session.attributes["curNode"] = 1
    session.attributes["prevNode"] = 0
    advice_q = '<speak>Do you want advice on an <emphasis>academic issue</emphasis>, or a <emphasis>personal issue</emphasis>?</speak>'
    getNodes()
    return question(advice_q)

@ask.intent("PersonalIssue")
def listPersonalIssues():
    session.attributes["curNode"] = 2
    session.attributes["prevNode"] = 1
    pIssues = "Personal issues go here."
    getNodes()
    return statement(pIssues)

@ask.intent("AcadIssue")
def listAcadIssues():
    session.attributes["curNode"] = 3
    session.attributes["prevNode"] = 1
    acadIssues = "Academic issues go here."
    getNodes()
    return statement(acadIssues)

def getNodes():
    print("Current node: " + str(session.attributes.get("curNode")) + ". Previous node: " + str(session.attributes.get("prevNode")) + ".")

if __name__ == "__main__":
    app.run(debug=True)
