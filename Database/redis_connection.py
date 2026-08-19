import redis
from Database import redis_config
from Database.redis_config import TTL
from schemas.task import *

r = redis.Redis(host = redis_config.HOST, port=redis_config.PORT, decode_responses=redis_config.DECODE_RESPONSE) #initiate redis server on port 6379 with decode reponse

def get_redis_connection():
    return redis.Redis(
        host=redis_config.HOST,
        port=redis_config.PORT,
        decode_responses=redis_config.DECODE_RESPONSE
    )




def invalidate_user_task_cache(user_id): # give user_id to delete because if you change the database you should delete the old redis cache
        pattern = f"tasks:user:{user_id}:*" # where user_id is add the argument
        for key in get_redis_connection().scan_iter(pattern): # loop through do r.scan_iter which is a function to filter the keys by pattern
                get_redis_connection().delete(key) # delete where this user_id... pattern is found











