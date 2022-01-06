from celery import Celery
import pymongo
import time
from bson import ObjectId

celery = Celery('task', broker='redis://redis:6379/0', backend='redis://redis:6379/0')

try:
  mongo = pymongo.MongoClient(host='mongodb', port=27017, serverSelectionTimeoutMS=1000)
  db = mongo.CloudSek
  mongo.server_info()
except:
  print ('Cannot connect to db')

@celery.task(ignore_result=False)
def processing(id, number1, number2):
  time.sleep(10)
  answer = number1 + number2
  db.Task.find_one_and_update({"_id": ObjectId(id)}, {'$set': {'answer': answer}})
  return answer
