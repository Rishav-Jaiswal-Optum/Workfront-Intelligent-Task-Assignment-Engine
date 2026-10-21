from workfront import *
from recommendation import *
import time

task = get_task("6accf87400014669583c23dc1cd51eef")
print(f"task: {task}")


recommendedUser = get_recommended_users(task)
print(f"Recommended User: {recommendedUser[0]}")

if not recommendedUser:
    print(
        "No user has qualified as per the task requirement"
    )
else:
    result = updateAssigment(task,recommendedUser[0])
    print(result)

