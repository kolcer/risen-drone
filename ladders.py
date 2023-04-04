import random
import time
import asyncio

from globals import *
from rated import *

def MG_RESET():
     
    MG_PLAYERS.clear()
    MG_QUEUE.clear()
    LADDERS['status'] = "off"
    LADDERS['channel'] = None
    LADDERS['currentPlayer'] = 0
    LADDERS['winDetect'] = 0
    
def MG_SHOW_STATS():

    
    toSend = "\nCurrent placements:\n"
    for plr, place in MG_PLAYERS.items():
        toSend += "**" + plr.name + "**: " + str(place) + " floor\n"
        if place > LADDERS['winDetect']:
            LADDERS['winDetect'] = place
    toSend += "-------------\n"
    return toSend

def MG_NEXT_PLAYER():
    LADDERS['currentPlayer'] += 1
    if LADDERS['currentPlayer'] > len(MG_QUEUE) - 1:
        LADDERS['currentPlayer'] = 0
      

def MG_SHOW_WINNERS():
    winners = []
    for i, v in MG_PLAYERS.items():
        if v >= LADDERS['topLevel']:
            winners.append(i)
                        
    toSend = winners[0].mention
    if len(winners) > 1:
        for i in range(1,len(winners)):
            toSend += " and " + winners[i].mention
    
    return toSend + " won LUCID LADDERS!"                    
    
def MG_ACTION(plr, action):
    
      
    #all players always advance 1 level per round
    for i in MG_PLAYERS.keys():
        MG_PLAYERS[i] += 1
        
    toSend = "All players advance 1 level.\n**" + plr.name + "** has played " + action + ". They "
    
    match action:
        case "none":
            toSend += "are chilling this round."
            
        case "muggle":
            chances = random.randint(0, 2)
            if chances == 2:
                MG_PLAYERS[plr] -= 1
                toSend += "got stuck and had to go down 1 level!"
            else:
                MG_PLAYERS[plr] += 1
                toSend += "did a stairjump trick, and advanced 1 extra level!"
                
        case "patron":
            ourLevel = MG_PLAYERS[plr]
            for i, v in MG_PLAYERS.items():
                if v <= ourLevel:
                    MG_PLAYERS[i] += 1
            toSend += "advanced 1 extra level with all other players below them."
                
        case "joker":
            victim = random.choice(MG_QUEUE)
            if victim != plr:
                toSend += "pranked " + victim.display_name + " - causing them to fell 2 levels down!"
                MG_PLAYERS[victim] -= 2
            else:
                toSend += "pranked themselves, and fell 1 level down."
                MG_PLAYERS[victim] -= 1
        
        case "wicked":
            ourLevel = MG_PLAYERS[plr]
            for i, v in MG_PLAYERS.items():
                if v > ourLevel:
                    MG_PLAYERS[i] -= 1
            toSend += "purged the stairs and above players fell one level."
            
        case "spectre":
            chances = random.randint(-1, 2)
            MG_PLAYERS[plr] += chances
            if chances == -1:
                toSend += "had a teleportation accident and lost one level!"
            elif chances == 0:
                toSend += "did not get any advantage."
            elif chances == 1:
                toSend += "teleported one extra level up."
            elif chances == 2:
                toSend += "teleported two extra levels up."
        
        case "keeper":
            toSend += "caused bottom player to advance an extra level and top player to go down!"
            top = None
            bottom = None
            topl = -99999999
            bottoml = 9999999
            for i, v in MG_PLAYERS.items():
               if v < bottoml:
                    bottom = i
                    bottoml = v
               if v > topl:
                    top = i
                    topl = v
            MG_PLAYERS[top] -=1
            MG_PLAYERS[bottom] += 1
            
        case "thief":
            victim = random.choice(MG_QUEUE)
            if victim != plr:
                toSend += "have stolen " + victim.display_name + " place!"
                cache = MG_PLAYERS[victim]
                MG_PLAYERS[victim] = MG_PLAYERS[plr]
                MG_PLAYERS[plr] = cache
            else:
                toSend += "have been caught stealing, and had to flee one level down!"
                MG_PLAYERS[plr] -= 1

        # balanced hacker - still gambling just more rigged ;)
        case "hacker":
            chances = random.randint(0, 3)
            if chances == 0 or chances == 1:
                toSend += "have been kicked from the game for hacking!"
                
                cp = MG_QUEUE[LADDERS['currentPlayer']]
                del MG_PLAYERS[plr]
                MG_QUEUE.remove(plr)
                LADDERS['currentPlayer'] = MG_QUEUE.index(cp)
                if len(MG_QUEUE) == 1:
                    MG_PLAYERS[cp] = LADDERS['topLevel']
                
            elif chances == 2:
                toSend += "have been frozen by a Murdurator and lost one level!"
                MG_PLAYERS[plr] -= 1
            else:
                toSend += "have hacked the game!"
                for i in MG_PLAYERS.keys():
                    MG_PLAYERS[i] -= 1
                MG_PLAYERS[plr] = LADDERS['topLevel']
                
        case "archon":
            toSend += "cast Split Event and caused players to either lose or gain an extra level or two."
            for i in MG_PLAYERS.keys():
                chances = random.randint(0,1)
                if chances == 0 or i == plr:
                    MG_PLAYERS[i] += random.randint(1,2)
                else:
                    MG_PLAYERS[i] -= random.randint(1, 2)
        
        case "drifter":
            chances = random.randint(0,1)
            if chances == 0:
                toSend += "took the elevator, but it was broken and a level was lost"
                MG_PLAYERS[plr] -= 1
            else:
                toSend += "took the elevator, and advanced 2 extra levels!"
                MG_PLAYERS[plr] += 2
                
        case "heretic":
            chances = random.randint(0,1)
            if chances == 0:
                toSend += "performed a dark ritual and swapped first and last players!"
                top = None
                bottom = None
                topl = -99999999
                bottoml = 9999999
                for i, v in MG_PLAYERS.items():
                    if v < bottoml:
                        bottom = i
                        bottoml = v
                    if v > topl:
                        top = i
                        topl = v
                cache = MG_PLAYERS[top]
                MG_PLAYERS[top] = MG_PLAYERS[bottom]
                MG_PLAYERS[bottom] = cache
            else:
                toSend += "failed to perform a dark ritual and got stranded - a level was lost."
                MG_PLAYERS[plr] -= 1
                
    return toSend

async def MG_LOOP(toSend):
    
    LADDERS['tick'] = time.time()
    ourTick = LADDERS['tick']
    
    while True:
        
        toSend += MG_SHOW_STATS()
        if LADDERS['winDetect'] >= LADDERS['topLevel'] or len(MG_QUEUE) < 2:
            toSend += MG_SHOW_WINNERS()
            await SEND(LADDERS['channel'], toSend)
            MG_RESET()
            return
        else:
            toSend += "**" + MG_QUEUE[LADDERS['currentPlayer']].name + "** turn! Choose Your alignment!"
            await SEND(LADDERS['channel'], toSend)
        
        await asyncio.sleep(LADDERS['maxWait'])
        
        if LADDERS['tick'] != ourTick:
            return
        
        cp = MG_QUEUE[LADDERS['currentPlayer']]
        MG_NEXT_PLAYER()
        toSend = MG_ACTION(cp,"none")

async def LucidLaddersProcessMessage(usr,msg):

       #mini game
    lmsg = msg.lower()
        
    if LADDERS['status'] == "gather" and lmsg == "begin" and usr == MG_QUEUE[0]:
            
        if len(MG_QUEUE) < 2:
            await SEND(LADDERS['channel'], "Not enough players for the Lucid Ladders to begin!")
            #return "Not enough players for the Lucid Ladders to begin!"
            return

        LADDERS['status'] = "on"
        await MG_LOOP("Lucid Ladders have begun!")            
            
        return
        
    elif LADDERS['status'] == "on" and lmsg in MG_SPELLS and MG_QUEUE[LADDERS['currentPlayer']] == usr:
        spell = lmsg
        while spell == "chameleon":
            spell = random.choice(MG_SPELLS)
        MG_NEXT_PLAYER()
        await MG_LOOP(MG_ACTION(usr,spell))

async def PlayLucidLadders(usr,ch):
        #mini game
 
    if LADDERS['status'] != "off":
        await SEND(ch, "A game is already in progress. Please wait for it to finish.")
        return
    else:
        LADDERS['status'] = "gather"
        MG_PLAYERS[usr] = 0
        MG_QUEUE.append(usr)
        LADDERS['currentPlayer'] = 0
        LADDERS['channel'] = ch
        LADDERS['tick'] = time.time()
        ourTick = LADDERS['tick']
        await SEND(ch, "<@&" + str(PING_ROLES["Minigames"].id) + ">\n" + usr.name + " has started new Lucid Ladders game! Type 'join' to join!\n" + usr.name + " - type 'begin' to start!")
        await asyncio.sleep(60)
        if LADDERS['status'] == "gather" and ourTick == LADDERS['tick']:
            await SEND(ch, "Lucid Ladders have been cancelled due to inactivity.")
            MG_RESET()
        return

async def JoinLucidLadders(usr):
    if usr in MG_PLAYERS:
        await SEND(LADDERS['channel'], "You have already joined the mini game!")
        return
    else:
        MG_PLAYERS[usr] = 0
        MG_QUEUE.append(usr)
        toSend = usr.name + " has joined Lucid Ladders! (You may leave by typing \'leave\')\nCurrent players:\n"
        for plr in MG_QUEUE:
            toSend += plr.name + "\n"
        await SEND(LADDERS['channel'], toSend)
        return

async def LeaveLucidLadders(usr):
    if usr in MG_PLAYERS:
        toSend = usr.name + " has left Lucid Ladders! :(\nCurrent players:\n"
        MG_PLAYERS.pop(MG_PLAYERS[usr])
        MG_QUEUE.pop(usr)
        for plr in MG_QUEUE:
            toSend += plr.name + "\n"
        await SEND(LADDERS['channel'], toSend)
        return
    else:
        await SEND(LADDERS['channel'], "You aren't in the game! Join by typing \'join\'! :D")
        return