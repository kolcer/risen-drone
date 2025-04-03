import random
import time
import asyncio

from globals import *
from rated import *
from database import *

def MG_RESET():
     
    MG_PLAYERS.clear()
    MG_QUEUE.clear()
    LADDERS['status'] = "off"
    LADDERS['channel'] = None
    LADDERS['currentPlayer'] = 0
    LADDERS['winDetect'] = 0
    LADDERS['playerCount'] = 0
    LADDERS['topLevel'] = 21
    LADDERS['tram']['travelers'] = []
    LADDERS['tram']['arrival'] = 7
    LADDERS['tram']['forward'] = True
    LADDERS['revival'] = {}
    LADDERS['revived'] = False
    LADDERS['kicked'] = False
    LADDERS['merges'] = []
    
def MG_SHOW_STATS():
    toSend = "\nCurrent placements:\n"
    for plr, place in MG_PLAYERS.items():
        # Find the pair (if it exists)
        pair = next((pair for pair in LADDERS["merges"] if plr in pair), None)

        if pair:            
            # Only display the pair once (when handling `pair[0]`)
            if plr == pair[0]:
                # Get the other player
                other_plr = pair[1] if pair[0] == plr else pair[0]
                toSend += f"**{plr.name} & {other_plr.name}**: {str(place)} floor"
            else:
                continue
        else:
            toSend += "**" + plr.name + "**: " + str(place) + " floor"

        if plr in LADDERS['tram']['travelers']:
            if LADDERS['tram']['forward']:
                toSend += f" (Tram⬆️, {LADDERS['tram']['arrival']} turns left)\n"
            else:
                toSend += f" (Tram⬇️, {LADDERS['tram']['arrival']} turns left)\n"
        else:
            toSend += "\n"
            
        if place > LADDERS['winDetect']:
            LADDERS['winDetect'] = place
    toSend += "-------------\n"
    return toSend

def MG_NEXT_PLAYER():
    if LADDERS['kicked']:
        LADDERS['kicked'] = False
        MG_PLAYERS.pop(MG_QUEUE[LADDERS['currentPlayer']])
        MG_QUEUE.pop(LADDERS['currentPlayer'])
        LADDERS['currentPlayer'] -= 1

    LADDERS['currentPlayer'] += 1

    if LADDERS['currentPlayer'] > len(MG_QUEUE) - 1:
        LADDERS['currentPlayer'] = 0

        #all players always advance 1 level per round
        for i in MG_PLAYERS.keys():
            MG_PLAYERS[i] += 1

        if len(LADDERS["tram"]["travelers"]) >= 1:
            if LADDERS['tram']['forward']:
                LADDERS["tram"]["arrival"] -= 1
            else:
                LADDERS["tram"]["arrival"] += 1

def MG_SHOW_WINNERS():
    finalMsg = ""
    winners = []
    for i, v in MG_PLAYERS.items():
        if v >= LADDERS['topLevel'] or len(MG_QUEUE) < 2:
            winners.append(i)
                        
    toSend = winners[0].mention
    if len(winners) > 1:
        for i in range(1,len(winners)):
            toSend += " and " + winners[i].mention

    if LADDERS["tram"]["arrival"] == 0:
        finalMsg = toSend + " had a nice trip to the orb and won LUCID LADDERS!"
    else:
        finalMsg = toSend + " won LUCID LADDERS!"
    
    return finalMsg                 
    
async def MG_ACTION(plr, action):
    toSend = ""
    match action:
        case "none":
            toSend += "are chilling this round."
        case "muggle":
            chances = random.randint(0, 5)
            if chances <= 2:
                toSend += "got stuck and did not climb any floor."
            elif chances <= 4:
                LADDERS['topLevel'] += 1
                UpdateFloor(plr, -1)
                # MG_PLAYERS[plr] -= 1
                toSend += "failed a Stairjump. The Drones felt the second-hand embarassment and created 1 more floor to the tower."
            else:
                LADDERS["topLevel"] += 2
                UpdateFloor(plr, 1)
                # MG_PLAYERS[plr] += 1
                toSend += "perfectly executed a Stairjump. The Drones were so impressed they added 2 more floors to the tower!"
                
        case "patron":
            ourLevel = MG_PLAYERS[plr]
            for i, v in MG_PLAYERS.items():
                if v <= ourLevel:
                    UpdateFloor(i, 1)
                    # MG_PLAYERS[i] += 1
            toSend += "advanced 1 extra level with all other players below them."
                
        case "joker":
            chances = random.randint(0,4)
            victim = SelectRandomUser(plr)

            if chances != 0:
                toSend += "pranked " + victim.name + " - causing them to fell 2 levels down!"
                # MG_PLAYERS[victim] -= 2
                UpdateFloor(victim, -2)
            else:
                toSend += "pranked themselves, and fell 1 level down."
                UpdateFloor(victim, -1)
                # MG_PLAYERS[victim] -= 1
        
        case "wicked":
            ourLevel = MG_PLAYERS[plr]
            for i, v in MG_PLAYERS.items():
                if v > ourLevel:
                    UpdateFloor(i, -1)
                    # MG_PLAYERS[i] -= 1
            toSend += "purged the stairs and above players fell one level."
            
        case "spectre":
            chances = random.randint(-1, 2)
            # MG_PLAYERS[plr] += chances
            UpdateFloor(plr, chances)
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
            # MG_PLAYERS[top] -=1
            # MG_PLAYERS[bottom] += 1
            UpdateFloor(top, -1)
            UpdateFloor(bottom, 1)
            
        case "thief":
            chances = random.randint(0,1)

            if chances == 0 or len(LADDERS["tram"]["travelers"]) < 1 or plr in LADDERS["tram"]["travelers"]:
                altchances = random.randint(0,4)
                victim = SelectRandomUser(plr)
                if altchances != 0:
                    toSend += "have stolen " + victim.name + "'s place!"
                    cache = MG_PLAYERS[victim]
                    # MG_PLAYERS[victim] = MG_PLAYERS[plr]
                    AssignFloor(victim, MG_PLAYERS[plr])
                    # MG_PLAYERS[plr] = cache
                    AssignFloor(plr, cache)
                else:
                    toSend += "have been caught stealing, and had to flee one level down!"
                    # MG_PLAYERS[plr] -= 1
                    UpdateFloor(plr, -1)
            else:
                stealChance = random.randint(0,3)

                if stealChance == 0:
                    LADDERS["tram"]["travelers"].clear()
                    LADDERS["tram"]["travelers"].append(plr)
                    toSend += "have stolen the tram, they are on their way to victory!"
                else:
                    lostLocation = random.randint(MG_PLAYERS[plr] - 3, MG_PLAYERS[plr] + 3)
                    # MG_PLAYERS[plr] = lostLocation
                    AssignFloor(plr, lostLocation)
                    toSend += "have miscalculated the tram's path and got lost in the tower!"
            
        case "hacker":
            chances = random.randint(0, 5)
            if chances >= 0 and chances <= 2:
                toSend += "have teleported next to the orb instead of inside it and fell to the bottom floor!"
                # MG_PLAYERS[plr] = 0
                AssignFloor(plr, 0)
                
            elif chances == 3:
                toSend += "have been frozen by a Murdurator and lost one level!"
                # MG_PLAYERS[plr] -= 1
                UpdateFloor(plr, -1)
            elif chances == 4:
                toSend += "have taken an upwards escalator and risen one level!"
                # MG_PLAYERS[plr] += 1
                UpdateFloor(plr, 1)
            else:
                toSend += "have hacked the game. All the thieves and heretics turn to look at them!"
                # MG_PLAYERS[plr] += 10
                UpdateFloor(plr, 10)
                
        case "archon":
            toSend += "cast Split Event and caused players to either lost or gain an extra level."
            for i in MG_PLAYERS.keys():
                chances = random.randint(0,1)
                if chances == 0 or i == plr:
                    # MG_PLAYERS[i] += 1
                    UpdateFloor(i, 1)
                else:
                    # MG_PLAYERS[i] -= 1
                    UpdateFloor(i, -1)
        
        case "drifter":
            chances = random.randint(0,1)
            if chances == 0:
                toSend += "took the elevator, but it was broken. A level was lost!"
                # MG_PLAYERS[plr] -= 1
                UpdateFloor(plr, -1)
            else:
                toSend += "took the elevator, and advanced 2 extra levels!"
                # MG_PLAYERS[plr] += 2
                UpdateFloor(plr, 2)
                
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
                # MG_PLAYERS[top] = MG_PLAYERS[bottom]
                AssignFloor(top, MG_PLAYERS[bottom])
                # MG_PLAYERS[bottom] = cache
                AssignFloor(bottom, cache)
            else:
                toSend += "failed to perform a dark ritual and got stranded - a level was lost."
                # MG_PLAYERS[plr] -= 1
                UpdateFloor(plr, -1)

        case "gremlin":
            chances = random.randint(0,4)
            curFloor = MG_PLAYERS[plr]

            if plr in LADDERS["tram"]["travelers"]:
                chances = 3

            if chances > 2:
                if len(LADDERS["tram"]["travelers"]) < 1:
                    for i, v in MG_PLAYERS.items():
                        if curFloor == v:
                            LADDERS["tram"]["travelers"].append(i)

                    toSend += "and everyone else on their floor hopped on the Tram. They will reach the destination in 7 turns!"
                else:
                    if plr not in LADDERS["tram"]["travelers"]:
                        # MG_PLAYERS[plr] -= 1
                        UpdateFloor(plr, -1)
                        toSend += "have missed the Tram and wasted 1 turn waiting for nothing."
                    else:
                        if LADDERS["tram"]["forward"]:
                            toSend += "have jumped and the Tram is now going backwards! Everyone inside loses 2 floors."

                            for trav in LADDERS["tram"]["travelers"]:
                                # MG_PLAYERS[trav] -= 2
                                UpdateFloor(trav, -2)
                        else:
                            toSend += "have jumped and the Tram is now back on track! Everyone inside gains 2 floors."

                            for trav in LADDERS["tram"]["travelers"]:
                                # MG_PLAYERS[trav] += 2
                                UpdateFloor(trav, 2)

                        LADDERS["tram"]["forward"] = not LADDERS["tram"]["forward"]
            else:
                subchances = random.randint(0,3)

                if subchances <= 1:
                    toSend += "have been waiting for the Tram to arrive, but it seems to be late."
                elif subchances == 2:
                    # MG_PLAYERS[plr] -= 1
                    UpdateFloor(plr, -1)
                    toSend += "are growing impatient and decided to check the previous stop."
                else:
                    # MG_PLAYERS[plr] += 1
                    UpdateFloor(plr, 1)
                    toSend += "are growing impatient and decided to check the next stop."

        case "necromancer":
            AssignRevival(plr, MG_PLAYERS[plr])

            toSend += "have created a Revival Point on their floor for good measure!"

        case "splicer":
            chances = random.randint(0,4)
            victim = SelectRandomUser(plr)

            if chances != 0:
                toSend += f"have spliced their floor with {victim.name}! They will meet in the middle."

                middle = (MG_PLAYERS[victim] + MG_PLAYERS[plr]) // 2
                # MG_PLAYERS[victim] = middle
                AssignFloor(victim, middle)
                # MG_PLAYERS[plr] = middle
                AssignFloor(plr, middle)
            else:
                toSend += "ended up in a twisted situation and lost 1 floor!"
                # MG_PLAYERS[plr] -= 1
                UpdateFloor(plr, -1)

        case "reaver":
            if len(MG_QUEUE) - (len(LADDERS["merges"]) * 2) == 1:
                toSend += "have broken the mirrors and lost 1 floor!"
                UpdateFloor(plr, -1)
            else:
                chances = random.randint(0,4)
                victim = SelectRandomUser(plr)

                if chances != 0 and not any(plr in pair for pair in LADDERS["merges"]) and not any(victim in pair for pair in LADDERS["merges"]):
                    toSend += f"have merged with {victim.name}! They are now one and the same."

                    SyncTeam(plr, victim)
                else:
                    toSend += "have forgotten a ghost is required to walk on mirrors and fell all the way down!"
                    # MG_PLAYERS[plr] = 0
                    AssignFloor(plr, 0)

        case "nothing":
            toSend += "have wasted everyone's time, I'll show them the door."


    toSend = "**Current top floor:** " + str(LADDERS['topLevel']) + "\n**`" + plr.name + "`** has played " + action + ". They " + toSend

    if LADDERS['currentPlayer'] == 0:     
        toSend = "All players advance 1 level.\n" + toSend

    if plr in MG_PLAYERS and MG_PLAYERS[plr] >= 31:
        if not str(plr.id) in list_decoded_entries("Pro Tower Climber"):
            await add_entry_with_check("Pro Tower Climber", plr)
            toSend += "\n**And they reached the 31th floor for the first time!**"
                
    return toSend

async def MG_LOOP(toSend):
    LADDERS['tick'] = time.time()
    ourTick = LADDERS['tick']
    
    while True:
        if LADDERS["tram"]["arrival"] == 0 and len(LADDERS["tram"]["travelers"]) > 0:
            for trav in LADDERS["tram"]["travelers"]:
                # MG_PLAYERS[trav] = LADDERS['topLevel']
                AssignFloor(trav, LADDERS['topLevel'])

        if MG_QUEUE[LADDERS['currentPlayer']] in LADDERS["revival"] and MG_PLAYERS[MG_QUEUE[LADDERS['currentPlayer']]] < LADDERS["revival"][MG_QUEUE[LADDERS['currentPlayer']]]:
            MG_PLAYERS[MG_QUEUE[LADDERS['currentPlayer']]] = LADDERS["revival"][MG_QUEUE[LADDERS['currentPlayer']]]
            LADDERS["revival"][MG_QUEUE[LADDERS['currentPlayer']]] = -100
            LADDERS['revived'] = True

        toSend += MG_SHOW_STATS()

        if LADDERS['winDetect'] >= LADDERS['topLevel'] or len(MG_QUEUE) < 2:
            toSend += MG_SHOW_WINNERS()
            await SEND(LADDERS['channel'], toSend)
            MG_RESET()
            return
        else:
            if LADDERS['revived']:
                toSend += "Your Revival Point brought you back up! But now it's gone.\n"
                LADDERS['revived'] = False

            toSend += MG_QUEUE[LADDERS['currentPlayer']].mention + "'s turn! Choose Your alignment!"
            await SEND(LADDERS['channel'], toSend)
        
        await asyncio.sleep(LADDERS['maxWait'])
        
        if LADDERS['tick'] != ourTick:
            return
        
        cp = MG_QUEUE[LADDERS['currentPlayer']]
        LADDERS["kicked"] = True
        MG_NEXT_PLAYER()
        toSend = await MG_ACTION(cp,"nothing")

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
        await MG_LOOP(await MG_ACTION(usr,spell))

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
        LADDERS['playerCount'] += 1
        if LADDERS['playerCount'] > 3:
            LADDERS['topLevel'] += 5
        MG_PLAYERS[usr] = 0
        MG_QUEUE.append(usr)
        toSend = usr.name + " has joined Lucid Ladders!\nCurrent players:\n"
        for plr in MG_QUEUE:
            toSend += plr.name + "\n"
        await SEND(LADDERS['channel'], toSend)
        return

def SelectRandomUser(usr):
    found = False

    # Find the paired user in LADDERS["merges"]
    paired_user = None
    for pair in LADDERS["merges"]:
        if usr in pair:
            paired_user = pair[0] if pair[1] == usr else pair[1]
            break

    # Ensure both the current user and the paired user are excluded from the random selection
    while not found:
        victim = random.choice(MG_QUEUE)
        
        # Check that the victim is not the current user or the paired user
        if victim != usr and victim != paired_user:
            found = True

    return victim

def UpdateFloor(usr, newfloor):
    pair = next((pair for pair in LADDERS["merges"] if usr in pair), None)

    if pair:
        MG_PLAYERS[pair[0]] += newfloor
        MG_PLAYERS[pair[1]] += newfloor
    else:
        MG_PLAYERS[usr] += newfloor

def AssignFloor(usr, newfloor):
    pair = next((pair for pair in LADDERS["merges"] if usr in pair), None)

    if pair:
        MG_PLAYERS[pair[0]] = newfloor
        MG_PLAYERS[pair[1]] = newfloor
    else:
        MG_PLAYERS[usr] = newfloor

def AssignRevival(usr, newfloor):
    pair = next((pair for pair in LADDERS["merges"] if usr in pair), None)

    if pair:
        LADDERS["revival"][pair[0]] = newfloor
        LADDERS["revival"][pair[1]] = newfloor
    else:
        MG_PLAYERS[usr] = newfloor

def SyncTeam(plr, victim):
    LADDERS["merges"].append([plr, victim])

    if plr in LADDERS["tram"]["travelers"]:
        LADDERS["tram"]["travelers"].append(victim)
    elif plr not in LADDERS["tram"]["travelers"] and victim in LADDERS["tram"]["travelers"]:
        LADDERS["tram"]["travelers"].remove(victim)

    if plr in LADDERS["revival"].keys():
        LADDERS["revival"][victim] = LADDERS["revival"][plr]
    elif plr not in LADDERS["revival"].keys() and victim in LADDERS["revival"].keys():
        LADDERS["revival"].pop(victim)

    AssignFloor(victim, MG_PLAYERS[plr])