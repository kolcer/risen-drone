<<<<<<< HEAD
import random
import time
import asyncio

from globals import *
from rated import *

def MG_RESET():
    global MG_STATUS
    global MG_CHANNEL 
    global MG_CURRENT_PLR 
    global MG_WIN_DETECT
    
    MG_PLAYERS.clear()
    MG_QUEUE.clear()
    MG_STATUS = "off"
    MG_CHANNEL = None
    MG_CURRENT_PLR = 0
    MG_WIN_DETECT = 0
    
def MG_SHOW_STATS():

    global MG_WIN_DETECT
    
    toSend = "\nCurrent placements:\n"
    for plr, place in MG_PLAYERS.items():
        toSend += "**" + plr.name + "**: " + str(place) + " floor\n"
        if place > MG_WIN_DETECT:
            MG_WIN_DETECT = place
    toSend += "-------------\n"
    return toSend

def MG_NEXT_PLAYER():
    global MG_CURRENT_PLR
    MG_CURRENT_PLR += 1
    if MG_CURRENT_PLR > len(MG_QUEUE) - 1:
        MG_CURRENT_PLR = 0
      

def MG_SHOW_WINNERS():
    winners = []
    for i, v in MG_PLAYERS.items():
        if v >= MINI_GAME_TOP_LEVEL:
            winners.append(i)
                        
    toSend = winners[0].mention
    if len(winners) > 1:
        for i in range(1,len(winners)):
            toSend += " and " + winners[i].mention
    
    return toSend + " won LUCID LADDERS!"                    
    
def MG_ACTION(plr, action):
    
    global MG_CURRENT_PLR 
     
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
            
        case "hacker":
            chances = random.randint(0, 3)
            if chances == 0:
                toSend += "have been kicked from the game for hacking!"
                
                cp = MG_QUEUE[MG_CURRENT_PLR]
                del MG_PLAYERS[plr]
                MG_QUEUE.remove(plr)
                MG_CURRENT_PLR = MG_QUEUE.index(cp)
                if len(MG_QUEUE) == 1:
                    MG_PLAYERS[cp] = MINI_GAME_TOP_LEVEL
                
            elif chances == 1:
                toSend += "have been frozen by a Murdurator and lost one level!"
                MG_PLAYERS[plr] -= 1
            elif chances == 2:
                toSend += "have had an unsuccessful hack, but was not detected!"
            else:
                toSend += "have hacked the game!"
                for i in MG_PLAYERS.keys():
                    MG_PLAYERS[i] -= 1
                MG_PLAYERS[plr] = MINI_GAME_TOP_LEVEL
                
        case "archon":
            toSend += "cast Split Event and caused players to either lost or gain a extra level."
            for i in MG_PLAYERS.keys():
                chances = random.randint(0,1)
                if chances == 0 or i == plr:
                    MG_PLAYERS[i] += 1
                else:
                    MG_PLAYERS[i] -= 1
        
        case "drifter":
            chances = random.randint(0,1)
            if chances == 0:
                toSend += "took the elevator, but it was broken - a level was lost"
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
    
    global MG_TICK
    MG_TICK = time.time()
    ourTick = MG_TICK
    
    while True:
        
        toSend += MG_SHOW_STATS()
        if MG_WIN_DETECT >= MINI_GAME_TOP_LEVEL or len(MG_QUEUE) < 2:
            toSend += MG_SHOW_WINNERS()
            await SEND(MG_CHANNEL, toSend)
            MG_RESET()
            return
        else:
            toSend += "**" + MG_QUEUE[MG_CURRENT_PLR].name + "** turn! Choose Your alignment!"
            await SEND(MG_CHANNEL, toSend)
        
        await asyncio.sleep(MINI_GAME_MAX_WAIT)
        
        if MG_TICK != ourTick:
            return
        
        cp = MG_QUEUE[MG_CURRENT_PLR]
        MG_NEXT_PLAYER()
        toSend = MG_ACTION(cp,"none")

async def LucidLaddersProcessMessage(usr,msg):

       #mini game
    global MG_STATUS
    lmsg = msg.lower()
        
    if MG_STATUS == "gather" and lmsg == "begin" and usr == MG_QUEUE[0]:
            
        if len(MG_QUEUE) < 2:
            await SEND(MG_CHANNEL, "Not enough players for the Lucid Ladders to begin!")
            #return "Not enough players for the Lucid Ladders to begin!"
            return

        MG_STATUS = "on"
        await MG_LOOP("Lucid Ladders have begun!")            
            
        return
        
    elif MG_STATUS == "on" and lmsg in MG_SPELLS and MG_QUEUE[MG_CURRENT_PLR] == usr:
        spell = lmsg
        while spell == "chameleon":
            spell = random.choice(MG_SPELLS)
        MG_NEXT_PLAYER()
        await MG_LOOP(MG_ACTION(usr,spell))

async def PlayLucidLadders(usr,ch):
        #mini game
    global MG_STATUS
    global MG_CHANNEL 
    global MG_CURRENT_PLR 
    global MG_TICK
 
    if MG_STATUS != "off":
        await SEND(ch, "A game is already in progress. Please wait for it to finish.")
        return
    else:
        MG_STATUS = "gather"
        MG_PLAYERS[usr] = 0
        MG_QUEUE.append(usr)
        MG_CURRENT_PLR = 0
        MG_CHANNEL = ch
        MG_TICK = time.time()
        ourTick = MG_TICK
        await SEND(ch, PING_ROLES["Minigames"].mention + "\n" + usr.name + " has started new Lucid Ladders game! Type 'join' to join!\n" + usr.name + " - type 'begin' to start!")
        await asyncio.sleep(60)
        if MG_STATUS == "gather" and ourTick == MG_TICK:
            await SEND(ch, "Lucid Ladders have been cancelled due to inactivity.")
            MG_RESET()
        return

async def JoinLucidLadders(usr):
  
    if usr in MG_PLAYERS:
        await SEND(MG_CHANNEL, "You have already joined the mini game!")
        return
    else:
        MG_PLAYERS[usr] = 0
        MG_QUEUE.append(usr)
        toSend = usr.name + " has joined Lucid Ladders!\nCurrent players:\n"
        for plr in MG_QUEUE:
            toSend += plr.name + "\n"
        await SEND(MG_CHANNEL, toSend)
        return
=======
import random
import time
import asyncio

from globals import *
from rated import *

def MG_RESET():
    global MG_STATUS
    global MG_CHANNEL 
    global MG_CURRENT_PLR 
    global MG_WIN_DETECT
    
    MG_PLAYERS.clear()
    MG_QUEUE.clear()
    MG_STATUS = "off"
    MG_CHANNEL = None
    MG_CURRENT_PLR = 0
    MG_WIN_DETECT = 0
    
def MG_SHOW_STATS():

    global MG_WIN_DETECT
    
    toSend = "\nCurrent placements:\n"
    for plr, place in MG_PLAYERS.items():
        toSend += "**" + plr.name + "**: " + str(place) + " floor\n"
        if place > MG_WIN_DETECT:
            MG_WIN_DETECT = place
    toSend += "-------------\n"
    return toSend

def MG_NEXT_PLAYER():
    global MG_CURRENT_PLR
    MG_CURRENT_PLR += 1
    if MG_CURRENT_PLR > len(MG_QUEUE) - 1:
        MG_CURRENT_PLR = 0
      

def MG_SHOW_WINNERS():
    winners = []
    for i, v in MG_PLAYERS.items():
        if v >= MINI_GAME_TOP_LEVEL:
            winners.append(i)
                        
    toSend = winners[0].mention
    if len(winners) > 1:
        for i in range(1,len(winners)):
            toSend += " and " + winners[i].mention
    
    return toSend + " won LUCID LADDERS!"                    
    
def MG_ACTION(plr, action):
    
    global MG_CURRENT_PLR 
     
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
            
        case "hacker":
            chances = random.randint(0, 3)
            if chances == 0:
                toSend += "have been kicked from the game for hacking!"
                
                cp = MG_QUEUE[MG_CURRENT_PLR]
                del MG_PLAYERS[plr]
                MG_QUEUE.remove(plr)
                MG_CURRENT_PLR = MG_QUEUE.index(cp)
                if len(MG_QUEUE) == 1:
                    MG_PLAYERS[cp] = MINI_GAME_TOP_LEVEL
                
            elif chances == 1:
                toSend += "have been frozen by a Murdurator and lost one level!"
                MG_PLAYERS[plr] -= 1
            elif chances == 2:
                toSend += "have had an unsuccessful hack, but was not detected!"
            else:
                toSend += "have hacked the game!"
                for i in MG_PLAYERS.keys():
                    MG_PLAYERS[i] -= 1
                MG_PLAYERS[plr] = MINI_GAME_TOP_LEVEL
                
        case "archon":
            toSend += "cast Split Event and caused players to either lost or gain a extra level."
            for i in MG_PLAYERS.keys():
                chances = random.randint(0,1)
                if chances == 0 or i == plr:
                    MG_PLAYERS[i] += 1
                else:
                    MG_PLAYERS[i] -= 1
        
        case "drifter":
            chances = random.randint(0,1)
            if chances == 0:
                toSend += "took the elevator, but it was broken - a level was lost"
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
    
    global MG_TICK
    MG_TICK = time.time()
    ourTick = MG_TICK
    
    while True:
        
        toSend += MG_SHOW_STATS()
        if MG_WIN_DETECT >= MINI_GAME_TOP_LEVEL or len(MG_QUEUE) < 2:
            toSend += MG_SHOW_WINNERS()
            await SEND(MG_CHANNEL, toSend)
            MG_RESET()
            return
        else:
            toSend += "**" + MG_QUEUE[MG_CURRENT_PLR].name + "** turn! Choose Your alignment!"
            await SEND(MG_CHANNEL, toSend)
        
        await asyncio.sleep(MINI_GAME_MAX_WAIT)
        
        if MG_TICK != ourTick:
            return
        
        cp = MG_QUEUE[MG_CURRENT_PLR]
        MG_NEXT_PLAYER()
        toSend = MG_ACTION(cp,"none")

async def LucidLaddersProcessMessage(usr,msg):

       #mini game
    global MG_STATUS
    lmsg = msg.lower()
        
    if MG_STATUS == "gather" and lmsg == "begin" and usr == MG_QUEUE[0]:
            
        if len(MG_QUEUE) < 2:
            await SEND(MG_CHANNEL, "Not enough players for the Lucid Ladders to begin!")
            #return "Not enough players for the Lucid Ladders to begin!"
            return

        MG_STATUS = "on"
        await MG_LOOP("Lucid Ladders have begun!")            
            
        return
        
    elif MG_STATUS == "on" and lmsg in MG_SPELLS and MG_QUEUE[MG_CURRENT_PLR] == usr:
        spell = lmsg
        while spell == "chameleon":
            spell = random.choice(MG_SPELLS)
        MG_NEXT_PLAYER()
        await MG_LOOP(MG_ACTION(usr,spell))

async def PlayLucidLadders(usr,ch):
        #mini game
    global MG_STATUS
    global MG_CHANNEL 
    global MG_CURRENT_PLR 
    global MG_TICK
 
    if MG_STATUS != "off":
        await SEND(ch, "A game is already in progress. Please wait for it to finish.")
        return
    else:
        MG_STATUS = "gather"
        MG_PLAYERS[usr] = 0
        MG_QUEUE.append(usr)
        MG_CURRENT_PLR = 0
        MG_CHANNEL = ch
        MG_TICK = time.time()
        ourTick = MG_TICK
        await SEND(ch, PING_ROLES["Minigames"].mention + "\n" + usr.name + " has started new Lucid Ladders game! Type 'join' to join!\n" + usr.name + " - type 'begin' to start!")
        await asyncio.sleep(60)
        if MG_STATUS == "gather" and ourTick == MG_TICK:
            await SEND(ch, "Lucid Ladders have been cancelled due to inactivity.")
            MG_RESET()
        return

async def JoinLucidLadders(usr):
  
    if usr in MG_PLAYERS:
        await SEND(MG_CHANNEL, "You have already joined the mini game!")
        return
    else:
        MG_PLAYERS[usr] = 0
        MG_QUEUE.append(usr)
        toSend = usr.name + " has joined Lucid Ladders!\nCurrent players:\n"
        for plr in MG_QUEUE:
            toSend += plr.name + "\n"
        await SEND(MG_CHANNEL, toSend)
        return
>>>>>>> 99a99fd4fc68704141506eab82f22c20f524dde0
