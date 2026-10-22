from flask import Flask, request
from engine import process_task

app = Flask(__name__)

@app.route("/process-task", methods=["POST"])

def process():

    task_id = request.json["taskID"]

    try:
        return process_task(task_id)
    except Exception as e:
        return {
            "success" : False,
            "error": str(e)
        }

app.run()