from datetime import date
import datetime
import calendar

# users = ['Dhruv', 'Ramya', 'Kiran']
users = [
            {"id" : 0, "name" : "Dhruv"},
            {"id" : 1, "name" : "Ramya"},
            {"id" : 2, "name" : "Kiran"}
        ]

status = [
            {"id" : 0, "name" : "Not Started"},
            {"id" : 1, "name" : "In Progress"},
            {"id" : 1, "name" : "Completed"}
        ]

tasks = [
            {"id" : 0, "name" : "Eric Homework"},
            {"id" : 1, "name" : "Book Reading"},
            {"id" : 2, "name" : "Music Practice"}, 
            {"id" : 3, "name" : "School Homework"},
            {"id" : 4, "name" : "Code Monkey"}, 
            {"id" : 5, "name" : "Cleaning House"},
            {"id" : 6, "name" : "Mopping"}
        ]

calendars = [
                {"id": 0, "name" : "Monday"},
                {"id": 1, "name" : "Tuesday"},
                {"id": 2, "name" : "Wednesday"},
                {"id": 3, "name" : "Thursday"},
                {"id": 4, "name" : "Friday"},
                {"id": 5, "name" : "Saturday"},
                {"id": 6, "name" : "Sunday"},
                {"id": 7, "name" : "Weekdays"},
                {"id": 8, "name" : "Weekends"},
                {"id": 9, "name" : "Daily"},
                {"id": 10, "name" : "Monthend"},
                {"id": 11, "name" : "Quarterend"},
                {"id": 12, "name" : "Scheduled"},
            ]
recurrence_pattern = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', 'Weekdays', 'Weekends', 'Daily',
                      'Monthend', 'Quarterend', 'Scheduled']

def GetUserName(user_id):
    for user in users:
        if (user["id"] == user_id):
            return user["name"]

def GetTaskName(task_id):
    for task in tasks:
        if (task["id"] == task_id):
            return task["name"]

def GetRecurrencePattern(calender_id_list):
    rec_pat_list = []
    for calendar_id in calender_id_list:
        rec_pat_list.append([cal["name"] for cal in calendars if cal["id"] == calendar_id])
    #Converting [[Sunday], [Monday], [Tuesday]] into ['Sunday', 'Monday', 'Tuesday']
    rec_pat_list = ([item for sublist in rec_pat_list for item in sublist]) 
    
    return rec_pat_list


def CheckValidCalendar(calendar_id: int):
    # print("CheckValidCalendar", calendar_id)
    curr_date = date.today()
    returnCode = 0
    rec_pat = ""
    for cal in calendars:
        if (cal["id"] == calendar_id):
            rec_pat = cal["name"]
            # print("match", rec_pat)
            break
    if rec_pat == 'Daily':
        returnCode = 1
    elif rec_pat == calendar.day_name[curr_date.weekday()]: #Check for day name
        returnCode = 1
    elif rec_pat == 'Weekdays' if (datetime.datetime.today().weekday() < 5) else 'Weekends':
        returnCode = 1
    # print("1: ", rec_pat, returnCode)
    return returnCode


def CheckValidRecurrence(rec_pat):
    curr_date = date.today()
    returnCode = 0
    if rec_pat == 'Daily':
        returnCode = 1
    elif rec_pat == calendar.day_name[curr_date.weekday()]: #Check for day name
        returnCode = 1
    elif rec_pat == 'Weekdays' if (datetime.datetime.today().weekday() < 5) else 'Weekends':
        returnCode = 1
    # print("2: ", rec_pat, returnCode)
    return returnCode

taskmap = [{"uid" : 0,
            "user_id" : 0,
            "task_id" : 0,
            "status_id" : 0,
            "calendar_id" : [6, 0, 1]
            # ,
            # "recurrence_pattern" : ["Sunday", "Monday", "Tuesday"]
           },
           {"uid" : 1,
            "user_id" : 0,
            "task_id" : 1,
            "status_id" : 0,
            "calendar_id" : [7]
            # ,
            # "recurrence_pattern" : ["Weekdays"]
           },
           {"uid" : 2,
            "user_id" : 0,
            "task_id" : 2,
            "status_id" : 0,
            "calendar_id" : [0, 2, 3, 4]
            # ,
            # "recurrence_pattern" : ["Monday", "Wednesday", "Thursday", "Friday"]
           },
           {"uid" : 3,
            "user_id" : 0,
            "task_id" : 4,
            "status_id" : 0,
            "calendar_id" : [6]
            # ,
            # "recurrence_pattern" : ["Sunday"]
           },
           {"uid" : 4,
            "user_id" : 2,
            "task_id" : 5,
            "status_id" : 1,
            "calendar_id" : [6, 2, 4, 9]
            # ,
            # "recurrence_pattern" : ["Wednesday", "Friday", "Sunday"]
           },
           {"uid" : 5,
            "user_id" : 2,
            "task_id" : 6,
            "status_id" : 0,
            "calendar_id" : [0]
            # ,
            # "recurrence_pattern" : ["Monday"]
           }
          ]
