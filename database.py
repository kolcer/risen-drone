import redis
import os
import random
from globals import FUN_ROLES, CHANNELS, EXTRA_ROLES, GIT_COMMITTERS, EVENTS
from rated import SEND

# Set up the data base
db = redis.from_url(os.environ.get("REDIS_URL"))

### PRIVATE SYNC FUNTIONS ###

def add_entry(key, new_entry):
    db.rpush(key,new_entry)

async def add_entry_with_check(key, new_entry):
    if not new_entry.id in GIT_COMMITTERS.values():
        roleCounter = 0

        for role in FUN_ROLES["Available"]:
            if str(new_entry.id) in list_decoded_entries(role):
                roleCounter += 1 
                break

        if roleCounter == 0:
            await SEND(CHANNELS["bot-commands"], f"{new_entry.name}, you just found your first secret role. Type `bd show profile` to view it.")

        db.rpush(key,new_entry.id)

async def add_egg_with_check(key, new_entry):
    eggCounter = 0

    for role in FUN_ROLES["Easter"]:
        if str(new_entry.id) in list_decoded_entries(role):
            eggCounter += 1 

    if eggCounter == 0:
        await SEND(CHANNELS["bot-commands"], f"{new_entry.name}, you just collected an egg! Thank you for the help. Type `bd show eggs` to look at it.")
    elif eggCounter == 5:
        db.rpush("Egg Collector",new_entry.id)

    db.rpush(key,new_entry.id)

def delete_key(key):
    db.delete(key)

def delete_entry(key, index):
    db.lset(key,index,"_del_")
    db.lrem(key,1,"_del_")

def delete_entry_by_value(key, value):
    db.lrem(key, 1, value)

def list_entries(key):
    result = db.lrange(key,0,-1)
    return result

def list_decoded_entries(key):
    result = db.lrange(key,0,-1)
    return [item.decode() for item in result]

def show_random_entry(key):
    index = random.randint(0,db.llen(key)-1)
    result = db.lrange(key,index,index)
    return result[0].decode("utf-8")

def get_amount_of_entries(key):
    return db.llen(key)

def show_specific_entry(key,index):
    result = db.lrange(key,index,index)
    return result[0].decode("utf-8")

def set_entry(key, value):
    db.set(key, value)

def get_value(key):
    value = db.get(key)
    if value is not None:
        return value.decode("utf-8")
    else:
        return None
    
def check_key(key):
    # Check if the key exists
    if db.exists(key):
        return True
    else:
        return False
    
def increment(key):
    return db.incr(key)

def redis_add_user_data(hash,key,value):
    db.hset(hash,key,value)