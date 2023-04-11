import redis
import os
import random
from globals import FUN_ROLES
# Set up the data base
db = redis.from_url(os.environ.get("REDIS_URL"))

### PRIVATE SYNC FUNTIONS ###

def add_entry(key, new_entry):
    db.rpush(key,new_entry)

# def add_entry_with_check(key, new_entry):   # finishing tomorrow
#     hadAtLeastOneRole = ""

#     for role in FUN_ROLES:
#         if new_entry in list_decoded_entries(role):
#             hadAtLeastOneRole = ", you just found your first secret role. Type `bd show profile` to view it."
#             break

#     db.rpush(key,new_entry)

#     return hadAtLeastOneRole

def delete_key(key):
    db.delete(key)

def delete_entry(key, index):
    db.lset(key,index,"_del_")
    db.lrem(key,1,"_del_")

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