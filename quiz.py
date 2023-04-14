import asyncio
import random

from globals import *
from rated import *
from database import *

class QuestionView(discord.ui.View):
    answer1 = None 
    answer2 = None 
    
    @discord.ui.select(
        placeholder="What is your age?",
        options=[
            discord.SelectOption(label="16 - 17", value="16"),
            discord.SelectOption(label="18 - 23", value="18"),
            discord.SelectOption(label="24 - 30", value="24")
        ]        
    )
    async def select_age(self, interaction:discord.Interaction, select_item : discord.ui.Select):
        self.answer1 = select_item.values
        self.children[0].disabled= True
        game_select = FavouriteGameSelect()
        self.add_item(game_select)
        await interaction.message.edit(view=self)
        await interaction.response.defer()

    async def respond_to_answer2(self, interaction : discord.Interaction, choices):
        self.answer2 = choices 
        self.children[1].disabled= True
        await interaction.message.edit(view=self)
        await interaction.response.defer()
        self.stop()

async def CLOSE_EVENT():
    print("entered")
    await asyncio.sleep(30)
    print("30 sec passed")
    if QUIZ["turn"] == QUIZ["cturn"] and QUIZ["active"]:
        print("same turns has been going on for 30 seconds")
        QUIZ["turn"] = 0
        QUIZ["cturn"] = -5
        QUIZ["active"] = False
        QUIZ["second-player"] = False
        QUIZ["can-answer"] = False
        QUIZ["rolls"].clear()
        QUIZ["scores"] = "**TOTAL POINTS**\n"
        QUIZZERS.clear()
        LOSERS.clear()
        return True

    print("not the same turn")
    QUIZ["cturn"] += 1
    return False

def FORCE_CLOSE_EVENT():
    QUIZ["turn"] = 0
    QUIZ["cturn"] = -5
    QUIZ["active"] = False
    QUIZ["second-player"] = False
    QUIZ["can-answer"] = False
    QUIZ["rolls"].clear()
    QUIZ["scores"] = "**TOTAL POINTS**\n"
    QUIZZERS.clear()
    LOSERS.clear()
    return

def showScores():
    for i in QUIZZERS:
        QUIZ["scores"] += str(i.display_name) + "'s points: " + str(QUIZZERS[i]) + "\n"
    return QUIZ["scores"]

#fetch questions from database. This is only done once per startup, so everytime question is added/removed/changed
#the bot needs to restart
async def FetchQuestions():
    entries = list_entries('quiz')
    for i in range(len(entries)):
        entry = entries[i].decode("utf-8")
        split = entry.split('|')
        QUESTIONS[str(i)] = [
            split[0],
            [split[1],split[2],split[3],split[4]],
            split[1],
            split[5],
            split[6]
        ]

async def nextQuestion(ch):
    usefulkeys = list(QUESTIONS.keys())
    QUIZ["rng"] = random.choice(usefulkeys)
    while QUIZ["rng"] in QUIZ["rolls"]:
        QUIZ["rng"] = random.choice(usefulkeys)

    QUIZ["rolls"].append(QUIZ["rng"])
    answers = ""
    qnum = "*Question no. " + str(QUIZ["turn"]) + "*\n"
    await SEND(ch, qnum + ":question: " + QUESTIONS[QUIZ["rng"]][0])

    random.shuffle(QUESTIONS[QUIZ["rng"]][1])   
    for i in QUESTIONS[QUIZ["rng"]][1]:
        answers += ":arrow_forward: `" + i + "` \n"

    await SEND(ch, answers)
    QUIZ["can-answer"] = True
    
    return

async def StartQuiz(usr,ch):
    #add user to the quiz users with 0 points.
    QUIZZERS[usr] = 0

    #activates the quiz, activates looking for second player.
    QUIZ["active"] = True
    QUIZ["second-player"] = True
    await SEND(ch, "<@&" + str(PING_ROLES["Minigames"].id) + ">\n" + usr.mention + " just started the Crazy Stairs Quiz!\nType 'join quiz' to begin with the questions. (BETA)")

    #if no one joins within 10 seconds, event is forced closed.
    await asyncio.sleep(30)
    if QUIZ["second-player"] == True:
        await SEND(ch, "Nobody joined in time. Event is concluded.")
        FORCE_CLOSE_EVENT()
    return

async def JoinQuiz(usr,ch):
    #disables looking for second player
    QUIZ["second-player"] = False
    #adds the new user to the quiz users
    QUIZZERS[usr] = 0
    #preparation to announce the two players
    users = list(QUIZZERS.keys())
    quizzerson = users[0].mention + " and " + users[1].mention + " have joined the Quiz. Questions are to follow. Good luck."
    await SEND(ch, quizzerson)
    #turn started from 0, now it begins
    QUIZ["turn"] += 1
    QUIZ["cturn"] = 1
    #prevents other people from talking while there is a quiz. avoids suggestions.
    #(this command cannot be used outside of bot-commands)
    await asyncio.sleep(2)
    await SEND(ch, "Beyond this point, any message sent from non-participating Users will be deleted.")
    #proceeds with the next(first in this case) question
    await asyncio.sleep(2)
    await nextQuestion(ch)
    #after starting, check if the round has been going on for more than 30 seconds.
    #if positive, close the event and send the message
    if await CLOSE_EVENT():
        await SEND(ch, "Event is concluded because both parts couldn't answer my very simple question.")
    return

async def ProcessQuizAnswer(usr,ch,message,lmsg):
    if usr not in QUIZZERS:
        await DELETE(message)
        return
            
    #if one of the two wants to stop they can feel free to
    if lmsg == "stop quiz":
        await SEND(ch, showScores() + usr.mention + " stopped the Quiz. Event is over.")
        FORCE_CLOSE_EVENT()
        return

    #each user gets one try at guessing the answer.
    #if you lost your attempt, wait for the other user to guess (or fail... concluding the event)
    if usr in LOSERS:
        await SEND(ch, "You have wasted your chance. Let the other User play now.")
        return

    #if the answer is not correct enter here
    if lmsg != QUESTIONS[QUIZ["rng"]][2].lower():
        #message is not correct but user is not in the LOSERS yet (otherwise code would have stopped before)
        #then a loser they become.
        if usr not in LOSERS:
          LOSERS.append(usr)

        #no return here. after adding a user, checks if both users are losers
        #if they are, the event gets forced closed.
        if len(LOSERS) == 2:
            await SEND(ch, showScores() + "Both players have not answered the question correctly. Event is over.")
            FORCE_CLOSE_EVENT()
            return

        #if it is the first user to get the answer wrong, then show broken's disappointment.
        await SEND(ch, QUESTIONS[QUIZ["rng"]][4])
        return

    #go here instead if the answer is not incorrect (which means it is correct indeed)
    #show broken's approval to the guessing user.
    QUIZ["can-answer"] = False
    finalmsg = ""
    if QUIZ["turn"] + 1 > len(QUESTIONS):
        finalmsg = QUESTIONS[QUIZ["rng"]][3]
    else:
        finalmsg = QUESTIONS[QUIZ["rng"]][3] + "\nBoth Players can now answer the next question."
    await SEND(ch, usr.mention + finalmsg)
    #the user who misguessed the answered gets a second chance (might it be the second or third depending on the round tho-)
    LOSERS.clear()
    #guesser gains 1 point
    QUIZZERS[usr] += 1
    #to the next turn we go (unless we want the same question to repeat itself)
    QUIZ["turn"] += 1
    await asyncio.sleep(5)

    #go here if there are no more questions
    if QUIZ["turn"] > len(QUESTIONS):
        highscore = -1
        for i in QUIZZERS:
            if QUIZZERS[i] > highscore:
                winner = i
                highscore = QUIZZERS[i]
            elif QUIZZERS[i] == highscore:
                await SEND(ch, showScores() + "That's a tie. But we do not like ties. Play again.")
                FORCE_CLOSE_EVENT()
                return

        #and the winner is (not you)
        await SEND(ch, showScores() + winner.mention + " correctly answered most of the questions and won the Event. Felicitations.")
        FORCE_CLOSE_EVENT()
        return

    #if there are more questions go here
    #after going to the next round check if the next round lasts more than 30 seconds
    await nextQuestion(ch)
    if await CLOSE_EVENT():
        await SEND(ch, showScores() + "Event is concluded because both parts couldn't answer my very simple question.")
    return      
