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
    if session.attributes["curNode"] == 0:
        session.attributes["curNode"] = 1
        session.attributes["prevNode"] = 0
        advice_q = '<speak>Do you want advice on an <emphasis>academic issue</emphasis>, or a <emphasis>personal issue</emphasis>?</speak>'
        getNodes()
        return question(advice_q)
    else:
        lastNode()

@ask.intent("learnMore")
def learnMore():
    if session.attributes["curNode"] == 0:
        session.attributes["curNode"] = 2
        session.attributes["prevNode"] = 0
        more_s = """<speak>The Student Wellbeing Centre, located on the First Floor of the Minerva Building, is here to offer support,
       advice and guidance with any issues or challenges that you may have during your studies. 
       Call us on <prosody rate="slow" volume="x-loud">'01522 837080'</prosody>, 
       or Email us at <prosody rate="slow" volume="x-loud">'studentsupport@lincoln.ac.uk'</prosody>. 
       Or you can visit us in person with our drop-in service from Monday to Friday during term-time, 
       between 12pm and 2pm, as well as on Thursday evenings between 5pm and 7pm.</speak>"""
        getNodes()
        return statement(more_s)
    else:
        lastNode()


@ask.intent("PersonalIssue")
def listPersonalIssues():
    if session.attributes["curNode"] == 1:
        session.attributes["curNode"] = 3
        session.attributes["prevNode"] = 1
        pIssues = "Personal issues go here."
        getNodes()
        return statement(pIssues)
    else:
        lastNode()

@ask.intent("AcadIssue")
def listAcadIssues():
    if session.attributes["curNode"] == 1:
        session.attributes["curNode"] = 4
        session.attributes["prevNode"] = 1
        acadIssues = "Academic issues go here."
        getNodes()
        return statement(acadIssues)
    else:
        lastNode()

def getNodes():
    print("Current node: " + str(session.attributes.get("curNode")) + ". Previous node: " + str(session.attributes.get("prevNode")) + ".")

#Map node ID numbers to their respective functions and call them if the current node value matches
def lastNode():
    if session.attributes["curNode"] == 0:
        start_skill()
    elif session.attributes["curNode"] == 1:
        getAdvice()
    elif session.attributes["curNode"] == 2:
        learnMore()
    elif session.attributes["curNode"] == 3:
        listPersonalIssues()
    elif session.attributes["curNode"] == 4:
        listAcadIssues()

if __name__ == "__main__":
    app.run(debug=True)