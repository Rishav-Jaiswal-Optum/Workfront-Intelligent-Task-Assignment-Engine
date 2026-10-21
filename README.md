# Workfront Intelligent Task Assignment Engine

## Overview

The Workfront Intelligent Task Assignment Engine automatically recommends and assigns the most suitable user to a Workfront task based on:

- Required Skill
- Required Experience
- User Skills
- User Experience
- User Availability

The solution integrates directly with Adobe Workfront APIs using OAuth JWT authentication and can automatically replace an existing assignee when task requirements change.

---

## Problem Statement

Task assignment is often performed manually and may not always account for:

- Resource skills
- Experience levels
- Current workload
- Resource availability

Additionally, task requirements can change after assignment.

Example:

```text
Task Assigned To: Writer

Skill Required changes:
Writer → Developer

Experience Required changes:
3 → 5
```

The original assignee may no longer be the best fit.

This solution automatically:

1. Evaluates task requirements
2. Finds qualified users
3. Calculates resource availability
4. Scores candidates
5. Selects the best resource
6. Reassigns the task if necessary

---

## Features

### Authentication

- OAuth JWT Authentication
- Adobe Workfront Machine-to-Machine Integration
- Secure access token generation

### User Qualification

- Skill-based filtering
- Experience validation
- Capacity validation

### Recommendation Engine

- User scoring
- User ranking
- Best candidate selection

### Assignment Automation

- Remove existing primary assignee
- Assign recommended resource
- Update task assignment in Workfront

---

## Architecture

```text
Task
 │
 ▼
Get Task Details
 │
 ▼
Get Users With Required Skill
 │
 ▼
Experience Validation
 │
 ▼
Capacity Validation
 │
 ▼
Score Qualified Users
 │
 ▼
Rank Users
 │
 ▼
Select Best Candidate
 │
 ▼
Remove Existing Assignment
 │
 ▼
Assign Recommended User
```

---

## Project Structure

```text
Workfront Intelligent Task Assignment Engine

│
├── .env
├── private.key
│
├── auth.py
├── config.py
├── workfront.py
├── recommendation.py
├── main.py
│
└── README.md
```

---

## Module Responsibilities

### auth.py

Responsible for authentication.

Functions:

```python
get_access_token()
```

Responsibilities:

- Generate JWT token
- Exchange JWT for Workfront access token

---

### config.py

Stores application configuration.

Examples:

```python
WORKFRONT_URL
CLIENT_ID
CLIENT_SECRET
CUSTOMER_ID
USER_ID
PUBLIC_KEY_ID
MAX_CAPACITY
```

---

### workfront.py

Responsible for all Workfront API interactions.

Functions:

```python
get_task()

get_users()

get_user_available_hours()

updateAssignment()
```

Responsibilities:

- Retrieve task details
- Retrieve users
- Calculate workload
- Update assignments

---

### recommendation.py

Contains recommendation business logic.

Functions:

```python
get_qualified_users()

get_user_score()

get_recommended_users()
```

Responsibilities:

- Filter qualified users
- Score candidates
- Rank candidates
- Return recommended user

---

### main.py

Application entry point.

Workflow:

```python
Task
 ↓
Recommendation Engine
 ↓
Assignment Update
```

---

## Workfront Custom Forms

### Task Custom Form

| Field | Purpose |
|---------|---------|
| Skill Required | Required skill |
| Experience | Minimum experience required |

Example:

```text
Skill Required = Developer
Experience = 2
```

---

### User Custom Form

| Field | Purpose |
|---------|---------|
| Skills | Multi-select skill list |
| Designer Experience | Experience level |
| Developer Experience | Experience level |
| Writer Experience | Experience level |

Example:

```text
Skills:
- Designer
- Developer

Designer Experience:
5
Developer Experience:
10
```

---

## Capacity Calculation

The engine evaluates assignments within a rolling two-week planning window.

Window:

```text
Beginning of current week
        ↓
End of next week
```

Maximum capacity:

```python
MAX_CAPACITY = 80
```

Representing:

```text
10 working days
×
8 hours
=
80 hours
```

Availability formula:

```python
available_hours =
MAX_CAPACITY -
assigned_hours
```

---

## User Qualification Rules

A user qualifies only when all conditions are met.

### Skill Match

```python
required_skill in user.skills
```

### Experience Match

```python
user_experience >= required_experience
```

### Capacity Match

```python
available_hours >= task_hours
```

---

## Scoring Algorithm

Current implementation:

```python
score =
(experience * 0.8) +
(availability * 0.2)
```

Example:

```python
{
    "user name": "Kim Brooks",
    "user experience": 10,
    "user availability": 80,
    "score": 24.0
}
```

Users are sorted in descending score order.

```python
sorted(
    users,
    key=lambda user: user["score"],
    reverse=True
)
```

---

## Assignment Logic

When a task already has a primary assignee:

```python
if task["primaryAssignment"]:
```

The engine:

```text
Delete Existing Assignment
        ↓
Assign Recommended User
```

This ensures the task is always assigned to the most suitable qualified resource.

---

## Example Workflow

### Initial Task

```text
Task Name: Task 1

Skill Required:
Writer

Experience:
3

Assigned To:
Ryan Oats
```

### Updated Task

```text
Skill Required:
Developer

Experience:
2
```

### Recommendation Result

```text
Recommended User:
Kim Brooks

Experience:
10

Availability:
80

Score:
24.0
```

### Action

```text
Remove Ryan Oats
        ↓
Assign Kim Brooks
```

### Result

```text
Task successfully reassigned in Workfront
```

---

## Technologies Used

- Python
- Requests
- PyJWT
- Adobe Workfront API
- OAuth JWT Authentication

---

## Results

✅ OAuth JWT Authentication

✅ Workfront API Integration

✅ Skill-Based Matching

✅ Experience-Based Matching

✅ Capacity-Based Validation

✅ User Scoring

✅ User Ranking

✅ Automatic Task Reassignment

✅ End-to-End Tested in Workfront Sandbox

---

## Future Enhancements

### V2

Event-Driven Automation

```text
Task Updated
        ↓
Workfront Event Subscription
        ↓
Recommendation Engine
        ↓
Automatic Reassignment
```

---

## Author

Project created as a proof-of-concept automation solution for intelligent task assignment within Adobe Workfront using custom forms, resource availability, experience-based scoring, and automated assignment/reassignment.