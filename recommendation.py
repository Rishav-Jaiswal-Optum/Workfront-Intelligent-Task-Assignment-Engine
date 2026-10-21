from workfront import *


def get_qualified_users(users, task, skill):
    
    qualifiedUsers=[]
    
    for user in users:

        if user[f"DE:API | {skill} Experience"] != None and user[f"DE:API | {skill} Experience"] >= task["DE:API | Experience"]:
            userAvailablity = get_user_available_hours(user["ID"])["availableHours"]
            if userAvailablity >= (task["workRequired"]/60):
                qualifiedUsers.append({"user":user, "availability":userAvailablity})\
    
    return qualifiedUsers
    

def get_user_score(experience,availability):
    return (experience * 0.8) + (availability*0.2)

def get_recommended_users(task):

    userScores = []
    skill = task["DE:API | Skill Required"]
    users = get_users(skill)

    for userObj in get_qualified_users(users, task, skill):

        score = get_user_score(userObj["user"][f"DE:API | {skill} Experience"], userObj["availability"])

        userScores.append({
            "user ID":userObj["user"]["ID"],
            "user name":userObj["user"]["name"], 
            "user email":userObj["user"]["emailAddr"], 
            "User Skill":task["DE:API | Skill Required"],
            "user experience":userObj["user"][f"DE:API | {skill} Experience"], 
            "user availability":userObj["availability"], 
            "score":score,
            })

    sortedUser = sorted(
        userScores,
        key=lambda user: user["score"],
        reverse=True
    )
    
    return sortedUser





