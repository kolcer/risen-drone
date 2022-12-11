import redis
import os
import random
# Set up the data base
db = redis.from_url(os.environ.get("REDIS_URL"))

### PRIVATE SYNC FUNTIONS ###

def add_entry(key, new_entry):
    db.rpush(key,new_entry)

def delete_entry(key, index):
    db.lset(key,index,"_del_")
    db.lrem(key,1,"_del_")

def list_entries(key):
    result = db.lrange(key,0,-1)
    return result

def show_random_entry(key):
    index = random.randint(0,db.llen(key)-1)
    result = db.lrange(key,index,index)
    return result[0].decode("utf-8")

def get_amount_of_entries(key):
    return db.llen(key)

def show_specific_entry(key,index):
    result = db.lrange(key,index,index)
    return result[0].decode("utf-8")

