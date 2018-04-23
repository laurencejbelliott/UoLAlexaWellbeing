from flask import Flask, Session
from flask_ask import Ask, question, statement, session

__author__ = 'Laurence Elliott'

app = Flask(__name__)
ask = Ask(app, "/")


@ask.launch
def start_skill():
    session.attributes["nodesVisited"] = {}
    session.attributes["nodesVisited"].update(
        {"HowAreYou": True,
        "feelingPositive": False,
        "feelingNegative": False,
        "emergency": False,
        "AcadIssue": False,
        "PersonalIssue": False,
        "GetAdvice": False}
    )
    welcome_message = '<speak>Welcome to the Student Wellbeing Centre Alexa skill. How are you feeling today?</speak>'
    return question(welcome_message)


@ask.session_ended
def session_ended():
    return "{}", 200


@ask.intent("AMAZON.HelpIntent")
def help():
    helpQ = '<speak>You can ask me to stop the skill by saying "stop", "cancel", or "exit".</speak>'
    return question(helpQ)


def invalidNodeChosen():
    session.attributes["nodesVisited"]["feelingPositive"] = True
    session.attributes["nodesVisited"]["feelingNegative"] = False
    invalidNodeChosenQ = "<speak>I'm sorry, I didn't understand you. Would you like help with an issue?</speak>"
    return question(invalidNodeChosenQ)


@ask.intent("feelingPositive")
def feelPositive():
    if session.attributes["nodesVisited"]["HowAreYou"]:
        session.attributes["nodesVisited"]["feelingPositive"] = True
        session.attributes["nodesVisited"]["feelingNegative"] = False
        feelPosQ = "<speak>That's good to hear. Would you like help with anything?</speak>"
        return question(feelPosQ)
    else:
        return invalidNodeChosen()

@ask.intent("feelingNegative")
def feelNegative():
    if session.attributes["nodesVisited"]["HowAreYou"] and not session.attributes["nodesVisited"]["GetAdvice"]:
        session.attributes["nodesVisited"]["feelingNegative"] = True
        session.attributes["nodesVisited"]["feelingPositive"] = False
        feelNegQ = "<speak>I'm sorry to hear that. Is your situation an emergency?</speak>"
        return question(feelNegQ)
    else:
        return invalidNodeChosen()

@ask.intent("AMAZON.YesIntent")
def yes():
    if session.attributes["nodesVisited"]["feelingNegative"]:
        return emergency()
    elif session.attributes["nodesVisited"]["feelingPositive"]:
        return getAdvice()
    else:
        return invalidNodeChosen()

@ask.intent("AMAZON.NoIntent")
def no():
    if session.attributes["nodesVisited"]["feelingNegative"]:
        return getAdvice()
    elif session.attributes["nodesVisited"]["feelingPositive"]:
        return goodbye()
    else:
        return invalidNodeChosen()


@ask.intent("emergency")
def emergency():
    session.attributes["nodesVisited"]["emergency"] = True
    emergencyS = '<speak>Please call the emergency services on <prosody rate="slow" volume="x-loud">9 9 9</prosody>, and/or campus security on <prosody rate="slow" volume="x-loud">0 1 5 2 2 <break time="1s"/> 8 8 <break time="1s"/> 6 0 6 2</prosody></speak>'
    return statement(emergencyS)

@ask.intent("GetAdvice")
def getAdvice():
    if session.attributes["nodesVisited"]["feelingPositive"] or session.attributes["nodesVisited"]["feelingNegative"]:
        session.attributes["nodesVisited"]["GetAdvice"] = True
        adviceQ = '<speak>Is your problem more of an <emphasis>academic issue</emphasis>, or a <emphasis>personal issue</emphasis>?</speak>'
        return question(adviceQ)
    else:
        return invalidNodeChosen()


@ask.intent("PersonalIssue")
def listPersonalIssues():
    if session.attributes["nodesVisited"]["GetAdvice"]:
        pIssues = "Personal issues go here."
        return statement(pIssues)
    else:
        return invalidNodeChosen()


@ask.intent("AcadIssue")
def listAcadIssues():
    if session.attributes["nodesVisited"]["GetAdvice"]:
        acadIssues = "Academic issues go here."
        return statement(acadIssues)
    else:
        return invalidNodeChosen()


def goodbye():
    return statement("<speak>Okay, have a nice day.</speak>")


@ask.intent("AMAZON.StopIntent")
def stop():
    return statement("It was nice speaking with you. Goodbye.")



@ask.intent("learnMore")
def learnMore():
    more_s = """<speak>The Student Wellbeing Centre, located on the Ground Floor of the Minerva Building, is here to offer support,
       advice and guidance with any issues or challenges that you may have during your studies. 
       Call us on <prosody rate="slow" volume="x-loud">'01522 837080'</prosody>, 
       or Email us at <prosody rate="slow" volume="x-loud">'studentsupport@lincoln.ac.uk'</prosody>. 
       Or you can visit us in person with our drop-in service from Monday to Friday during term-time, 
       between 12pm and 2pm, as well as on Thursday evenings between 5pm and 7pm.</speak>"""
    return statement(more_s)


if __name__ == "__main__":
    app.run(debug=True)
