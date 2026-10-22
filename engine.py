from workfront import get_task, updateAssignment
from recommendation import get_recommended_users

def process_task(task_id):

    task = get_task(task_id)

    recommended_users = get_recommended_users(task)

    if not recommended_users:
        return {
            "success": False,
            "message": "No qualified users found"
        }

    return updateAssignment(
        task,
        recommended_users[0]
    )