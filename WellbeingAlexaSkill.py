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
        "financeOrLegal": False,
        "bullyingHarassment" : False
         }
    )

    # session attribute created to store an ordered array of the node names
    # for personal issues' nodes
    session.attributes["personalIssuesOrdered"] = [
        "crisis",
        "disabilityOrCond",
        "financeOrLegal",
        "bullyingHarassment"
    ]

    # session attribute created to store an ordered array of the node names
    # for academic issues' nodes
    session.attributes["academicIssuesOrdered"] = [
        "maths",
        "writing",
        "offencesAndAppeals"
    ]
    welcome_message = '<speak>Welcome to the Student Wellbeing Centre Alexa skill. How are you feeling today?</speak>'
    return question(welcome_message)


@ask.session_ended
def session_ended():
    return "{}", 200


@ask.intent("AMAZON.HelpIntent")
def help():
    helpS = '<speak>You can ask me to stop the skill at any time by saying "stop", "cancel", or "exit". ' \
            'You can talk with me turn-by-turn to find your problem and get advice, ' \
            'or you can tell me your problem, for example: "I\'m being bullied", ' \
            'and get our advice for the problem directly. Lastly you can launch ' \
            'the skill with: "Alexa, tell student wellbeing..." and whatever you' \
            'would like to say to the student wellbeing skill, for example: ' \
            '"Alexa, tell student wellbeing I need advice on plagiarism".</speak>'
    return statement(helpS)

# returns true if the all of the personal issue nodes before it have been visited,
# and the parameter node has not been visited.
def personalIssueIsNextNode(nodeName):
    nodeIndex = session.attributes["personalIssuesOrdered"].index(nodeName)
    for i in range(0,nodeIndex - 1):
        if not session.attributes["nodesVisited"][session.attributes["personalIssuesOrdered"][i]]:
            return False
    if not session.attributes["nodesVisited"][nodeName]:
        return True
    else:
        return False

# returns true if the all of the personal issue nodes before it have been visited,
# and the parameter node has been visited, and the personal issue nodes after the
# parameter node have not been visited.
def personalIssueIsCurrentNode(nodeName):
    nodeIndex = session.attributes["personalIssuesOrdered"].index(nodeName)
    for i in range(0,nodeIndex):
        if not session.attributes["nodesVisited"][session.attributes["personalIssuesOrdered"][i]]:
            return False
    if [session.attributes["personalIssuesOrdered"][nodeIndex+1]] != None:
        for i in range(nodeIndex+1,len(session.attributes["personalIssuesOrdered"])-1):
            if session.attributes["nodesVisited"][session.attributes["personalIssuesOrdered"][i]]:
                return False
    return True

# returns true if the all of the academic issue nodes before it have been visited,
# and the parameter node has not been visited.
def academicIssueIsNextNode(nodeName):
    nodeIndex = session.attributes["academicIssuesOrdered"].index(nodeName)
    for i in range(0,nodeIndex - 1):
        if not session.attributes["nodesVisited"][session.attributes["academicIssuesOrdered"][i]]:
            return False
    if not session.attributes["nodesVisited"][nodeName]:
        return True
    else:
        return False

# returns true if the all of the academic issue nodes before it have been visited,
# and the parameter node has been visited, and the academic issue nodes after the
# parameter node have not been visited.
def academicIssueIsCurrentNode(nodeName):
    nodeIndex = session.attributes["academicIssuesOrdered"].index(nodeName)
    for i in range(0,nodeIndex):
        if not session.attributes["nodesVisited"][session.attributes["academicIssuesOrdered"][i]]:
            return False
    if [session.attributes["academicIssuesOrdered"][nodeIndex+1]] != None:
        for i in range(nodeIndex+1,len(session.attributes["academicIssuesOrdered"])-1):
            if session.attributes["nodesVisited"][session.attributes["academicIssuesOrdered"][i]]:
                return False
    return True

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
         "crisis": False,
         "disabilityOrCond": False,
         "financeOrLegal": False,
         "bullyingHarassment": False
         }
    )
    invalidNodeChosenQ = "<speak>I'm sorry, I didn't understand you. Would you like help with an issue?</speak>"
    return question(invalidNodeChosenQ)


@ask.intent("feelingPositive")
def feelPositive():
    session.attributes["personalIssuesOrdered"] = [
        "crisis",
        "disabilityOrCond",
        "financeOrLegal",
        "bullyingHarassment"
    ]

    session.attributes["academicIssuesOrdered"] = [
        "maths",
        "writing",
        "offencesAndAppeals"
    ]
    try:
        if not (session.attributes["nodesVisited"]["GetAdvice"]):
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
                 "financeOrLegal": False,
                 "bullyingHarassment": False
                 }
            )
    except:
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
             "financeOrLegal": False,
             "bullyingHarassment": False
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
    session.attributes["personalIssuesOrdered"] = [
        "crisis",
        "disabilityOrCond",
        "financeOrLegal",
        "bullyingHarassment"
    ]

    session.attributes["academicIssuesOrdered"] = [
        "maths",
        "writing",
        "offencesAndAppeals"
    ]
    try:
        if (not (session.attributes["nodesVisited"]["GetAdvice"])):
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
                 "financeOrLegal": False,
                 "bullyingHarassment": False
                 }
            )
    except:
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
             "financeOrLegal": False,
             "bullyingHarassment": False
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
          and (session.attributes["nodesVisited"]["feelingPositive"]
               or session.attributes["nodesVisited"]["feelingNegative"])
          and session.attributes["nodesVisited"]["GetAdvice"]):
        # the first if statement evaluates whether the last personal issue node
        # has been visited
        if session.attributes["nodesVisited"]["offencesAndAppeals"]:
            return offencesAndAppealsHelp()
        elif academicIssueIsCurrentNode("maths"):
            return mathsHelp()
        elif academicIssueIsCurrentNode("writing"):
            return writingHelp()
    #If statements for returning advice for personal issues
    elif (session.attributes["nodesVisited"]["PersonalIssue"]
          and (session.attributes["nodesVisited"]["feelingPositive"]
               or session.attributes["nodesVisited"]["feelingNegative"])
          and session.attributes["nodesVisited"]["GetAdvice"]):
        if session.attributes["nodesVisited"]["bullyingHarassment"]:
            return bullyingHarassmentHelp()
        elif personalIssueIsCurrentNode("crisis"):
            return crisisHelp()
        elif personalIssueIsCurrentNode("disabilityOrCond"):
            return disabilityOrCondHelp()
        elif personalIssueIsCurrentNode("financeOrLegal"):
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
        if academicIssueIsNextNode("writing"):
            return writing()
        elif academicIssueIsNextNode("offencesAndAppeals"):
            return offencesAndAppeals()
    #if statements for moving down the list of personal issues
    elif session.attributes["nodesVisited"]["PersonalIssue"]:
        if personalIssueIsNextNode("disabilityOrCond"):
            return disabilityOrCond()
        elif personalIssueIsNextNode("financeOrLegal"):
            return financeOrLegal()
        elif personalIssueIsNextNode("bullyingHarassment"):
            return bullyingHarassment()
    else:
        return invalidNodeChosen()


@ask.intent("emergency")
def emergency():
    emergencyS = '<speak>Please call the emergency services on <prosody rate="slow" volume="x-loud">9 9 9</prosody>, and / or campus security on <prosody rate="slow" volume="x-loud">0 1 5 2 2 <break time="0.10s"/> 8 8 <break time="0.10s"/> 6 0 6 2</prosody></speak>'
    return statement(emergencyS)

@ask.intent("GetAdvice")
def getAdvice():
    session.attributes["personalIssuesOrdered"] = [
        "crisis",
        "disabilityOrCond",
        "financeOrLegal",
        "bullyingHarassment"
    ]

    session.attributes["academicIssuesOrdered"] = [
        "maths",
        "writing",
        "offencesAndAppeals"
    ]
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
         "financeOrLegal": False,
         "bullyingHarassment": False
         }
    )
    if session.attributes["nodesVisited"]["feelingPositive"] or session.attributes["nodesVisited"]["feelingNegative"]:
        session.attributes["nodesVisited"]["GetAdvice"] = True
        adviceQ = '<speak>Is your problem more of an <emphasis>academic</emphasis> issue, or a <emphasis>personal</emphasis> issue?</speak>'
        return question(adviceQ)
    else:
        return invalidNodeChosen()


@ask.intent("PersonalIssue")
def listPersonalIssues():
    session.attributes["nodesVisited"] = {}
    session.attributes["nodesVisited"].update(
        {"HowAreYou": True,
         "feelingPositive": False,
         "feelingNegative": True,
         "AcadIssue": False,
         "PersonalIssue": True,
         "GetAdvice": True,
         "maths": False,
         "writing": False,
         "offencesAndAppeals": False,
         "crisis": False,
         "disabilityOrCond": False,
         "financeOrLegal": False,
         "bullyingHarassment": False
         }
    )
    session.attributes["personalIssuesOrdered"] = [
        "crisis",
        "disabilityOrCond",
        "financeOrLegal",
        "bullyingHarassment"
    ]

    session.attributes["academicIssuesOrdered"] = [
        "maths",
        "writing",
        "offencesAndAppeals"
    ]
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


def bullyingHarassment():
    session.attributes["nodesVisited"]["bullyingHarassment"] = True
    bullyingHarassmentQ = "Do you think you might be a victim of bullying or harassment?"
    return question(bullyingHarassmentQ)

@ask.intent("bullyingHarassment")
def bullyingHarassmentHelp():
    bullyingHarassmentS = "<speak>For help with bullying or harassment, call the student support centre on" \
    " <prosody rate=\"slow\" volume=\"x-loud\">01522 837080</prosody> or send us an email to " \
    "<prosody rate=\"slow\" volume=\"x-loud\">studentsupport@lincoln.ac.uk</prosody>.</speak>"
    return statement(bullyingHarassmentS)
############################


@ask.intent("AcadIssue")
def listAcadIssues():
    session.attributes["nodesVisited"] = {}
    session.attributes["nodesVisited"].update(
        {"HowAreYou": True,
         "feelingPositive": False,
         "feelingNegative": True,
         "AcadIssue": True,
         "PersonalIssue": False,
         "GetAdvice": True,
         "maths": False,
         "writing": False,
         "offencesAndAppeals": False,
         "crisis": False,
         "disabilityOrCond": False,
         "financeOrLegal": False,
         "bullyingHarassment": False
         }
    )

    session.attributes["personalIssuesOrdered"] = [
        "crisis",
        "disabilityOrCond",
        "financeOrLegal",
        "bullyingHarassment"
    ]

    session.attributes["academicIssuesOrdered"] = [
        "maths",
        "writing",
        "offencesAndAppeals"
    ]
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
