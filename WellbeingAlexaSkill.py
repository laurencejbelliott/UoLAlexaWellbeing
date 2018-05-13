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
        "AcadIssue": False,
        "PersonalIssue": False,
        "GetAdvice": False,
        "maths": False,
        "writing": False,
        "offencesAndAppeals": False,
        "crisis": False,
        "disabilityOrCond": False,
        "financeOrLegal": False
         }
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
    session.attributes["nodesVisited"].update(
        {"HowAreYou": True,
         "feelingPositive": True,
         "feelingNegative": False,
         "AcadIssue": False,
         "PersonalIssue": False,
         "GetAdvice": False,
         "maths": False,
         "writing": False,
         "offencesAndAppeals": False,
         "crisis" : False,
         "disabilityOrCond": False,
         "financeOrLegal": False
         }
    )
    invalidNodeChosenQ = "<speak>I'm sorry, I didn't understand you. Would you like help with an issue?</speak>"
    return question(invalidNodeChosenQ)


@ask.intent("feelingPositive")
def feelPositive():
    try:
        if not (session.attributes["nodesVisited"]["GetAdvice"]):
            session.attributes["nodesVisited"] = {}
            session.attributes["nodesVisited"].update(
                {"HowAreYou": True,
                 "feelingPositive": True,
                 "feelingNegative": False,
                 "AcadIssue": False,
                 "PersonalIssue": False,
                 "GetAdvice": False,
                 "maths": False,
                 "writing": False,
                 "offencesAndAppeals": False,
                 "crisis": False,
                 "disabilityOrCond": False,
                 "financeOrLegal": False
                 }
            )
    except:
        session.attributes["nodesVisited"] = {}
        session.attributes["nodesVisited"].update(
            {"HowAreYou": True,
             "feelingPositive": True,
             "feelingNegative": False,
             "AcadIssue": False,
             "PersonalIssue": False,
             "GetAdvice": False,
             "maths": False,
             "writing": False,
             "offencesAndAppeals": False,
             "crisis": False,
             "disabilityOrCond": False,
             "financeOrLegal": False
             }
        )
    if session.attributes["nodesVisited"]["HowAreYou"]:
        session.attributes["nodesVisited"]["feelingPositive"] = True
        session.attributes["nodesVisited"]["feelingNegative"] = False
        feelPosQ = "<speak>That's good to hear. Would you like help with anything?</speak>"
        return question(feelPosQ)
    else:
        return invalidNodeChosen()

@ask.intent("feelingNegative")
def feelNegative():
    try:
        if (not (session.attributes["nodesVisited"]["GetAdvice"])):
            session.attributes["nodesVisited"] = {}
            session.attributes["nodesVisited"].update(
                {"HowAreYou": True,
                 "feelingPositive": False,
                 "feelingNegative": True,
                 "AcadIssue": False,
                 "PersonalIssue": False,
                 "GetAdvice": False,
                 "maths": False,
                 "writing": False,
                 "offencesAndAppeals": False,
                 "crisis": False,
                 "disabilityOrCond": False,
                 "financeOrLegal": False
                 }
            )
    except:
        session.attributes["nodesVisited"] = {}
        session.attributes["nodesVisited"].update(
            {"HowAreYou": True,
             "feelingPositive": False,
             "feelingNegative": True,
             "AcadIssue": False,
             "PersonalIssue": False,
             "GetAdvice": False,
             "maths": False,
             "writing": False,
             "offencesAndAppeals": False,
             "crisis": False,
             "disabilityOrCond": False,
             "financeOrLegal": False
             }
        )
    if session.attributes["nodesVisited"]["HowAreYou"] and not session.attributes["nodesVisited"]["GetAdvice"]:
        session.attributes["nodesVisited"]["feelingNegative"] = True
        session.attributes["nodesVisited"]["feelingPositive"] = False
        feelNegQ = "<speak>I'm sorry to hear that. Is your situation an emergency?</speak>"
        return question(feelNegQ)
    else:
        return invalidNodeChosen()

@ask.intent("AMAZON.YesIntent")
def yes():
    if session.attributes["nodesVisited"]["feelingNegative"] and not session.attributes["nodesVisited"]["GetAdvice"]:
        return emergency()
    elif session.attributes["nodesVisited"]["feelingPositive"] and not session.attributes["nodesVisited"]["GetAdvice"]:
        return getAdvice()
    #If statements for returning advice for academic issues
    elif (session.attributes["nodesVisited"]["AcadIssue"]
          and (session.attributes["nodesVisited"]["FeelingPositive"]
               or session.attributes["nodesVisited"]["FeelingNegative"])
          and session.attributes["nodesVisited"]["GetAdvice"]):
        if session.attributes["nodesVisited"]["maths"] and not session.attributes["nodesVisited"]["writing"]:
            return mathsHelp()
        elif session.attributes["nodesVisited"]["maths"] and session.attributes["nodesVisited"]["feelingNegative"] and not session.attributes["nodesVisited"]["writing"]:
            return mathsHelp()
        elif session.attributes["nodesVisited"]["maths"] and session.attributes["nodesVisited"]["feelingPositive"] and not session.attributes["nodesVisited"]["writing"]:
            return mathsHelp()
        elif (session.attributes["nodesVisited"]["writing"] and session.attributes["nodesVisited"]["maths"]
              and (session.attributes["nodesVisited"]["feelingPositive"] or session.attributes["nodesVisited"]["feelingNegative"])
              and not session.attributes["nodesVisited"]["offencesAndAppeals"]):
            return writingHelp()
        elif (session.attributes["nodesVisited"]["maths"]
              and session.attributes["nodesVisited"]["writing"]
              and session.attributes["nodesVisited"]["offencesAndAppeals"]):
            return offencesAndAppealsHelp()
    #If statements for returning advice for personal issues
    elif (session.attributes["nodesVisited"]["PersonalIssue"]
          and (session.attributes["nodesVisited"]["feelingPositive"]
               or session.attributes["nodesVisited"]["feelingNegative"])
          and session.attributes["nodesVisited"]["GetAdvice"]):
        if (session.attributes["nodesVisited"]["crisis"]
         and not session.attributes["nodesVisited"]["disabilityOrCond"]):
            return crisisHelp()
        elif (session.attributes["nodesVisited"]["crisis"]
         and session.attributes["nodesVisited"]["disabilityOrCond"]
         and not session.attributes["nodesVisited"]["financeOrLegal"]):
            return disabilityOrCondHelp()
        elif (session.attributes["nodesVisited"]["crisis"]
         and session.attributes["nodesVisited"]["disabilityOrCond"]
         and session.attributes["nodesVisited"]["financeOrLegal"]):
            return financeOrLegalHelp()
    else:
        return invalidNodeChosen()

@ask.intent("AMAZON.NoIntent")
def no():
    if (session.attributes["nodesVisited"]["feelingNegative"]
        and not (session.attributes["nodesVisited"]["maths"]
        or session.attributes["nodesVisited"]["crisis"])
    ):
        return getAdvice()
    elif session.attributes["nodesVisited"]["feelingPositive"] and not (session.attributes["nodesVisited"]["maths"] or session.attributes["nodesVisited"]["crisis"]):
        return goodbye()
    #if statements for moving down the list of academic issues
    elif session.attributes["nodesVisited"]["AcadIssue"]:
        if session.attributes["nodesVisited"]["maths"] and not session.attributes["nodesVisited"]["writing"]:
            return writing()
        elif (session.attributes["nodesVisited"]["maths"]
              and session.attributes["nodesVisited"]["writing"]
              and not session.attributes["nodesVisited"]["offencesAndAppeals"]):
            return offencesAndAppeals()
    #if statements for moving down the list of academic isues
    elif session.attributes["nodesVisited"]["PersonalIssue"]:
        if (session.attributes["nodesVisited"]["crisis"]
            and not session.attributes["nodesVisited"]["disabilityOrCond"]):
            return disabilityOrCond()
        elif (session.attributes["nodesVisited"]["crisis"]
              and session.attributes["nodesVisited"]["disabilityOrCond"]
              and not session.attributes["nodesVisited"]["financeOrLegal"]):
            return financeOrLegal()
    else:
        return invalidNodeChosen()


@ask.intent("emergency")
def emergency():
    emergencyS = '<speak>Please call the emergency services on <prosody rate="slow" volume="x-loud">9 9 9</prosody>, and / or campus security on <prosody rate="slow" volume="x-loud">0 1 5 2 2 <break time="0.10s"/> 8 8 <break time="0.10s"/> 6 0 6 2</prosody></speak>'
    return statement(emergencyS)

@ask.intent("GetAdvice")
def getAdvice():
    if session.attributes["nodesVisited"]["feelingPositive"] or session.attributes["nodesVisited"]["feelingNegative"]:
        session.attributes["nodesVisited"]["GetAdvice"] = True
        adviceQ = '<speak>Is your problem more of an <emphasis>academic</emphasis> issue, or a <emphasis>personal</emphasis> issue?</speak>'
        return question(adviceQ)
    else:
        return invalidNodeChosen()


@ask.intent("PersonalIssue")
def listPersonalIssues():
    if session.attributes["nodesVisited"]["GetAdvice"]:
        session.attributes["nodesVisited"]["PersonalIssue"] = True
        return crisis()
    else:
        return invalidNodeChosen()

##### PERSONAL ISSUES ######


def crisis():
    session.attributes["nodesVisited"]["crisis"] = True
    crisisQ = "<speak>Are you, or is someone you know, in a crisis?</speak>"
    return question(crisisQ)

@ask.intent("crisis")
def crisisHelp():
    crisisS = '<speak>If there is an imminent threat to life,' \
    ' or an emergency, please call the emergency services on ' \
    '<prosody rate="slow" volume="x-loud">9 9 9</prosody>, ' \
    'and / or campus security on ' \
    '<prosody rate="slow" volume="x-loud">0 1 5 2 2 <break time="0.10s"/> 8 8 <break time="0.10s"/> 6 0 6 2</prosody>. ' \
    'Otherwise if you are finding that your mental health is ' \
    'affecting your ability to study, please come to a drop-in ' \
    'session at the Student Wellbeing Centre in the Minerva building ' \
    'as soon as possible.</speak>'
    return statement(crisisS)

def disabilityOrCond():
    session.attributes["nodesVisited"]["disabilityOrCond"] = True
    disabilityOrCondQ = "<speak>Do you want help with a disability or medical condition?</speak>"
    return question(disabilityOrCondQ)

@ask.intent("disabilityOrCond")
def disabilityOrCondHelp():
    disabilityOrCondS = '<speak>For help with a disability or medical/psychiatric condition,' \
    'Contact the student wellbeing team located in the ' \
    'Minerva building, next to the MHT building. For extra information you can ' \
    'call: <prosody rate="slow" volume="x-loud">01522 886400</prosody> or send ' \
    'them an email at: ' \
    '<prosody rate="slow" volume="x-loud">studentwellbeing@lincoln.ac.uk</prosody>. ' \
    'You can also visit the university health service to book an appointment with a GP. ' \
    'Contact details, open-times, and other useful information about the health service ' \
    'can be found at <prosody rate="slow" volume="x-loud">' \
    '<say-as interpret-as=\"spell-out\">ulhs</say-as>online.co.uk' \
    '</prosody>.</speak>'
    return statement(disabilityOrCondS)

def financeOrLegal():
    session.attributes["nodesVisited"]["financeOrLegal"] = True
    financeOrLegalQ = "<speak>Do you want help with a financial or legal matter?</speak>"
    return question(financeOrLegalQ)

@ask.intent("financeOrLegal")
def financeOrLegalHelp():
    financeOrLegalS = '<speak>The advice service offers students free and' \
    'confidential legal and financial advice. Go to the student support centre, ' \
    'on the ground floor of the Minerva building and ask for the advice service. ' \
    'Drop-in times are Monday to Friday, 12pm to 2pm. You can also book an appointment ' \
    'by emailing <emphasis>adviceappointments@lincoln.ac.uk</emphasis>.</speak>'
    return statement(financeOrLegalS)

############################


@ask.intent("AcadIssue")
def listAcadIssues():
    if session.attributes["nodesVisited"]["GetAdvice"]:
        session.attributes["nodesVisited"]["AcadIssue"] = True
        return maths()
    else:
        return invalidNodeChosen()


##### ACADEMIC ISSUES #####

def maths():
    session.attributes["nodesVisited"]["maths"] = True
    mathsQ = "<speak>Do you want extra help with maths?</speak>"
    return question(mathsQ)

@ask.intent("maths")
def mathsHelp():
    mathsHelpS = "MASH: Maths and Statistics Help, in the Learning Development " \
                 "room, on the ground floor of the library," \
                 " offers free one-to-one advice. " \
                 "See their page on the University of Lincoln library " \
                 "website for up to date drop-in times and contact details. " \
                 "You can also see them by appointment," \
                 " by emailing 'mash@lincoln.ac.uk'."
    return statement(mathsHelpS)

def writing():
    session.attributes["nodesVisited"]["writing"] = True
    writingQ = "Do you want help with academic reading, writing, referencing or research?"
    return question(writingQ)

@ask.intent("writing")
def writingHelp():
    writingHelpS = "Learning Development on the ground floor" \
                   " of the library offers academic writing support " \
                   "drop-in sessions. Up to date drop-in times and " \
                   "contact details are available on the library website's " \
                   "Learning Development page, as well as information about workshops."
    return statement(writingHelpS)

def offencesAndAppeals():
    session.attributes["nodesVisited"]["offencesAndAppeals"] = True
    offencesAndAppealsQ = "Do you want advice on plagiarism, " \
                          "extenuating circumstances," \
                          "extensions, complaints, " \
                          "appeals or withdrawal of services?"
    return question(offencesAndAppealsQ)

@ask.intent("offencesAndAppeals")
def offencesAndAppealsHelp():
    offencesAndAppealsHelpS = "<speak>For advice on academic offences, extenuating " \
    "circumstances, complaints, or withdrawal of services," \
    "call the student support centre on" \
    " <prosody rate=\"slow\" volume=\"x-loud\">01522 837080</prosody> or send us an email to " \
    "<prosody rate=\"slow\" volume=\"x-loud\">studentsupport@lincoln.ac.uk</prosody>. " \
    "The student’s union advice centre is " \
    "able to help you as well on <prosody rate=\"slow\" volume=\"x-loud\">01522 837000</prosody> " \
    "or send them an email " \
    "to <prosody rate=\"slow\" volume=\"x-loud\">'advice@lincoln<say-as interpret-as=\"spell-out\">su</say-as>.com'</prosody>.</speak>"
    return statement(offencesAndAppealsHelpS)
###########################


def goodbye():
    return statement("<speak>Okay, have a nice day.</speak>")

@ask.intent("AMAZON.RepeatIntent")
def repeat():
    return invalidNodeChosen()

@ask.intent("AMAZON.StopIntent")
def stop():
    return statement("It was nice speaking with you. Goodbye.")

if __name__ == "__main__":
    app.run(debug=True)
