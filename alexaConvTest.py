from flask import Flask
from flask_ask import Ask, question, statement

__author__ = 'Laurence Elliott'

app = Flask(__name__)
ask = Ask(app, "/")

@ask.launch
def start_skill():
    welcome_message = "elcomeway... Speak a phrase in English and ask me to translate it into Pig Latin"
    return question(welcome_message).simple_card(content="Elcomeway! Speak a phrase in English and ask me to translate it into Pig Latin.")


@ask.intent("AMAZON.HelpIntent")
def help():
    return question("You can speak a phrase in English and ask me to translate it into Pig Latin..."
                    "For example: What is hello in Pig Latin..."
                    "Or you can ask me to stop the skill by saying 'stop', 'cancel', or 'exit'")


@ask.intent("AMAZON.StopIntent")
def stop():
    return statement("Goodbye")


@ask.intent("GetPigLatin", mapping={'eng_phrase':'ENGPhrase'})
def trans_into_pl(eng_phrase):
    eng_words = eng_phrase.split()
    pl_transd_words = []
    consonants = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'y',
                  'z']
    vowels = ['a', 'e', 'i', 'o', 'u']
    numbers = [0,1,2,3,4,5,6,7,8,9]
    numbersPlurals = ["0s","1s","2s","3s","4s","5s","6s","7s","8s","9s"]
    numberWords = ['zero','one','two','three','four','five','six','seven','eight','nine']
    for i in range(0, len(eng_words)):
        current_word = eng_words[i].replace('\'','')
        try:
            if int(eng_words[i]) in numbers:
                current_word = numberWords[int(eng_words[i])]
        except:
            pass
        if eng_words[i] in numbersPlurals:
            current_word = numberWords[int(eng_words[i][0])] + "s"

        if current_word[0].lower() in vowels:
            pl_transd_words.append(current_word + "ay")
        elif current_word[0:1].lower() in consonants and current_word[1:2].lower() in consonants and len(current_word) > 2:
            pl_transd_words.append(current_word[2:] + current_word[0:2].lower() + "ay")
        else:
            pl_transd_words.append(current_word[1:] + current_word[0:1].lower() + "ay")
    return statement('Translating {} into pig latin'.format(eng_phrase)+
                     "...Your phrase in pig latin is {}".format(" ".join(pl_transd_words))).simple_card(content="Your phrase in pig latin is {}".format(" ".join(pl_transd_words)))

if __name__ == "__main__":
    app.run(debug=True)