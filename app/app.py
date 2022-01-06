from flask import Flask, Response
import pymongo
from celery import Celery
from bson import ObjectId

app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'redis://redis:6379/0'
app.config['CELERY_BACKEND_URL'] = 'redis://redis:6379/0'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'], backend=app.config['CELERY_BACKEND_URL'])
celery.conf.update(app.config)

try:
  mongo = pymongo.MongoClient(host='mongodb', port=27017, serverSelectionTimeoutMS=1000)
  db = mongo.CloudSek
  mongo.server_info()
except:
  print ('Cannot connect to db')

# Main route
@app.route('/', methods=['GET'])
def index():
  return Response(
    response='Hello from test API',
    status=200
  )

# Calculation route
@app.route('/calculate/<int:num1>/<int:num2>', methods=['GET'])
def add(num1, num2):
  data = {"number1": num1, "number2": num2, "answer": None}
  dbRes = db.Task.insert_one(data)
  id = f"{dbRes.inserted_id}"
  r = celery.send_task('task.processing', kwargs={"id": id, "number1": num1, "number2": num2})
  return Response(
    response = id + ' ' + str(r.id),
    status = 200
  )

# Answer route
@app.route("/status/<string:id>")
def status(id):
  res = celery.AsyncResult(id, app=celery)
  return str(res.state)

# Answer route
@app.route("/get_answer/<string:id>")
def answer(id):
  doc = db.Task.find_one({"_id": ObjectId(id)})
  if doc == None:
    return Response(
      response='Invalid ID',
      status=404
    )
  elif doc['answer'] == None:
    return Response(
      response='Please wait',
      status=200
    )
  return Response(
    response=str(doc["answer"]),
    status=200
  )

if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0')
