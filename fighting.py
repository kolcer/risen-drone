import random
import time
import asyncio

from globals import *
from rated import *

def FG_RESET():
    FG_PLAYERS.clear()
    FG_QUEUE.clear()
    FG['status'] = "off"
    FG['currentPlayer'] = 0
    FG['tick'] = 0

async def PlayFightingGame(usr, ch):
        #mini game
 
    if FG['status'] != "off":
        await SEND(ch, "A match is already in progress.")
        return
    else:
        FG['status'] = "second-player"
        FG_PLAYERS[usr] = [None, None, 70] #class, status, accuracy
        FG_QUEUE.append(usr)
        FG['currentPlayer'] = 0
        FG['tick'] = time.time()
        ourTick = FG['tick']
        await SEND(ch, "<@&" + str(PING_ROLES["Minigames"].id) + ">\n" + usr.name + " has started a fight! Type 'join fight' to battle!")
        await asyncio.sleep(60)
        if FG['status'] == "second-player" and ourTick == FG['tick']:
            await SEND(ch, "Nobody joined in time.")
            FG_RESET()
        return

async def JoinFightingGame(usr, ch):

    if usr in FG_PLAYERS:
        await SEND(FG['channel'], "Wait for someone else.")
        return
    else:
        FG_PLAYERS[usr] = [None, None, 70] #class, status, accuracy
        FG_QUEUE.append(usr)
        await SEND(ch, usr.name + " is eager to battle too.")
        return
