import requests
import urllib3
from functools import reduce
import time

from config import *
from auth import get_access_token

urllib3.disable_warnings()

def get_header():
    
    token = get_access_token()

    return {
        "sessionID": token
    }


# Get Task Details
def get_task(task_id):

    try:
        response = requests.get(
            f"{WORKFRONT_URL}/attask/api/v20.0/task/{task_id}",
            headers=get_header(),
            params={
                "fields":"name,status,workRequired,DE:API | Skill Required,DE:API | Experience, assignedToID, assignmentsListString, primaryAssignment:ID"
            },
            verify=False
        )

        return response.json()["data"]

    except Exception as e:
        print(f"error: {str(e)}")

# Get all designers
def get_users(skill):
     
    try:
        response = requests.get(
            f"{WORKFRONT_URL}/attask/api/v21.0//user/search?DE:API | Skills={skill}&DE:API | Skills_Mod=contains",
            headers=get_header(),
            params={
                "fields":f"name, emailAddr, title, DE:API | Skills, DE:API | {skill} Experience"
            },
            verify=False
        )

        print("Status:", response.status_code)

        return response.json()["data"]
    
    except Exception as e:
        print(f"error: {str(e)}")

# Get Assigned Planned Hours for User

def get_user_available_hours(user_id):

    try:
        assignmentHours = requests.get(
            f"{WORKFRONT_URL}/attask/api/v21.0/ASSGN/search?OR:1:assignedToID={user_id}&OR:1:status=CPL&OR:1:status_Mod=ne&OR:1:task:plannedStartDate=$$TODAYbw&OR:1:task:plannedStartDate_Range=$$TODAYew+7d&OR:1:task:plannedStartDate_Mod=between&OR:2:opTask:plannedStartDate=$$TODAYbw&OR:2:opTask:plannedStartDate_Range=$$TODAYew+7d&OR:2:opTask:plannedStartDate_Mod=between&OR:2:assignedToID={user_id}&OR:2:status=CPL&OR:2:status_Mod=ne",
            headers=get_header(),
            params={
                "fields":"workRequired, taskID, opTaskID"
            },
            verify=False
        )

        TotalAssignedHours = 0
        for assignment in assignmentHours.json()["data"]:
            TotalAssignedHours += assignment["workRequired"]

        return {
            "assigned_hours":(TotalAssignedHours/60),
            "availableHours":MAX_CAPACITY - (TotalAssignedHours/60)
        }

    except Exception as e:
        print(f"error: {str(e)}")

# Update Task Assignment
def updateAssigment(task,user):
    
    if task.get("primaryAssignment"):
        try:
            removeAssignment = requests.delete(
            f"{WORKFRONT_URL}/attask/api/v21.0/ASSGN/{task["primaryAssignment"]["ID"]}",
            headers=get_header(),
            verify=False
            )    
            print("Delete Status:",
            removeAssignment.status_code)

        except Exception as e:
            print(f"error: {str(e)}")

    try:
        updateTask = requests.put(
            f"{WORKFRONT_URL}/attask/api/v21.0/task/{task["ID"]}",
            headers=get_header(),
            json={
                "assignedToID": user["user ID"]
            },
            verify=False
        )

        return {
            "success": updateTask.status_code == 200,
            "Updated Task":f"Task '{updateTask.json()["data"]["name"]}' reassigned",
            "User Assigned": user["user name"]
        }

    except Exception as e:
        print(f"error: {str(e)}")


    
    
