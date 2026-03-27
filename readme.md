📋 Task Manager API
Build a simple task management API where:

Users can register and login
Only logged in users can manage their tasks
Each user can only see their own tasks

Routes to build:
MethodRouteActionPOST/registerRegister a userPOST/loginLogin and get tokenGET/tasksGet all your tasksPOST/tasksAdd a new taskPUT/tasks/<id>Update a taskDELETE/tasks/<id>Delete a task
Each task should have:

id → auto generated
title → task title
done → True or False (is it completed?)
username → who owns this task

Create a new file called tasks.py and start fresh. Don't copy from app.py — try to build it yourself using what you learned!
Start with the basics first — imports, get_db(), and the tasks table in your database.