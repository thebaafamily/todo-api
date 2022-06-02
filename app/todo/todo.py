# Import pandas library
from asyncio import tasks
from todo import tasksmeta as tm
import pandas as pd
import numpy as np

class TaskUtil:
    dfTasksMetaData = pd.DataFrame()
    dfTasksToday = pd.DataFrame()
    taskReset = True

    def __GetTasks(self) -> pd.DataFrame:
        # if self.dfTasksToday.empty:
        if self.taskReset:
            self.taskReset = False
            self.__InitTasks()
        return self.dfTasksToday
    
    def __InitTasks(self) -> pd.DataFrame:
        print('Initializing Tasks...')
        self.dfTasksMetaData = pd.json_normalize(data=tm.taskmap)
        self.dfTasksToday = self.dfTasksMetaData.copy()
        return self.__PruneTasks()

    def __PruneTasks(self) -> pd.DataFrame:
        print('Pruning Tasks...')
        valid_for_today_df = pd.json_normalize(data=tm.calendars)
        valid_for_today_df['is_valid'] = valid_for_today_df.apply(lambda row: tm.CheckValidCalendar(row['id']), axis=1 )
        
        self.__GetTasks()
        # print("Pruning default", self.dfTasksToday)
        self.dfTasksToday['user_name'] = self.dfTasksToday.apply(lambda row: tm.GetUserName(row['user_id']), axis=1 )
        # print("Pruning with user_name ", self.dfTasksToday)
        self.dfTasksToday['task_name'] = self.dfTasksToday.apply(lambda row: tm.GetTaskName(row['task_id']), axis=1 )
        # print("Pruning with task_name ", self.dfTasksToday)
        self.dfTasksToday['recurrence_pattern'] = self.dfTasksToday.apply(lambda row: tm.GetRecurrencePattern(row['calendar_id']), axis=1)
        # print("Pruning with recurrence_pattern ", self.dfTasksToday)
        self.dfTasksToday['is_valid'] = self.dfTasksToday.apply(lambda row: int(any(x in row['calendar_id'] for x in valid_for_today_df[valid_for_today_df['is_valid'] == 1]['id'].to_list())), axis=1)
        # print("Pruning with is_valid ", self.dfTasksToday)
        # print(self.dfTasksToday[['uid', 'task_name', 'user_name', 'recurrence_pattern']])
        return self.dfTasksToday
    
    def GetUsersList(self) -> dict:
        return tm.users

    def GetTaskList(self) -> dict:
        return tm.tasks

    def GetCalendarList(self) -> dict:
        return tm.calendars
    
    def GetTasks(self) -> dict:
        tasks_df = self.__GetTasks()
        tasks_df = tasks_df[tasks_df['is_valid']==1][['uid', 'user_id', 'user_name', 'task_id', 'task_name', 'status_id', 'recurrence_pattern']]
        return tasks_df.to_dict('records')

    def GetTasksForTodayUserId(self, user_id: int) -> dict:
        tasks_df = self.__GetTasks()
        tasks_df = tasks_df[tasks_df['is_valid']==1][['uid', 'user_id', 'user_name', 'task_id', 'task_name', 'status_id', 'recurrence_pattern']]
        # print("result", tasks_df)
        return tasks_df[tasks_df['user_id'] == user_id].to_dict('records')

    def UpdateTaskForward(self, uid: int):
        self.dfTasksToday['status_id'] = self.dfTasksToday.apply(lambda row: row['status_id']+1 if (row['uid'] == uid) else row['status_id'], axis=1)
        user_id = self.dfTasksToday[self.dfTasksToday['uid'] == uid]['user_id'].tolist()[0]
        return self.GetTasksForTodayUserId(user_id)

    def GetTasksMetadata(self):
        tasks_df = self.__GetTasks()
        tasks_df = tasks_df[['uid', 'user_id', 'user_name', 'task_id', 'task_name', 'recurrence_pattern']]
        # print(tasks_df)
        return tasks_df.to_dict('records')

    def UpdateTaskBackward(self, uid: int):
        self.dfTasksToday['status_id'] = self.dfTasksToday.apply(lambda row: row['status_id']-1 if (row['uid'] == uid) else row['status_id'], axis=1 )
        user_id = self.dfTasksToday[self.dfTasksToday['uid'] == uid]['user_id'].tolist()[0]
        return self.GetTasksForTodayUserId(user_id)

    def GetTasksForUserId(self, user_id: int):
        tasks_df = self.__GetTasks()
        return tasks_df[tasks_df['user'] == user_id]

    def AssignTask(self, request: dict):
        nextuid = max(([m['uid'] for m in tm.taskmap])) + 1
        data ={"uid" : nextuid,
               "user_id" : request["user_id"],
               "task_id" : request["task_id"],
               "status_id" : 0,
               "calendar_id" : request["calendar_id"]
           }
        tm.taskmap.append(data)
        self.taskReset = True
        a = self.__GetTasks()
        return self.__GetTasks().to_dict('records')
