# ProTracker
#### Video Demo:  <https://youtu.be/p8rmKLhZgpk?si=9zfV2n32fgM3guS8>
#### Description:
ProTracker: A Streamlined Project Management Tool

ProTracker is a user-friendly Python web application designed to empower you to manage projects, collaborate with team members, and track your progress efficiently. It acts as a central hub for organizing your tasks, setting deadlines, and keeping everyone on the same page.

##### Key Features:
> Intuitive Task Management: ProTracker allows you to create and manage individual tasks within projects. Assign tasks to yourself or team members, ensuring clarity and accountability.

> Deadline-Driven Focus: Set clear due dates for each task, promoting goal-oriented work and timely completion.

> Collaborative Workflow: Create projects, delegate tasks to team members, and foster seamless collaboration, ideal for both small and large teams.

> Progress Tracking and Transparency: Track your completed tasks and visualize your progress over time. ProTracker provides a sense of accomplishment and fosters motivation.

> Streamlined User Interface: The clean and intuitive interface makes navigating ProTracker a breeze. Find the features you need quickly and stay focused on getting things done.

##### Project Structure:

> templates: Houses HTML templates for the user interface:

>> Index:
>>> - Which shows the assigned tasks of the user with due date.
>>> - User can directly mark the task "In Progress" or "Completed" from the Index tab itself.

>> Create A New Project:
>>> - Helps the user to create a new project and insert it into the SQL datatbase.
>>> - User Needs to input the **Project Title**, **Start Date**, and **Description**.
>>> - Once the new project is created the website is redirected to **Projects Page**.

>>Create A New Task:
>>> - Helps the user to create a new task in a project and assigne it theselves or to other users.
>>> - User needs to input the *Task Name*, *Username* of the user to whom the task is being assiged to, and the *due date* for the task.
>>> - Once created the task page is redirected to the Index page.

>>Projects:
>>> - Shows the ongoing projects and their details.
>>> - The user can mark the project as Completed or in progress from the projects tab itself.
>>> - Clicking on a project will redirect the user to the project details page for that project.

>>History:
>>> - Show the completed task of the user with the date of completion.
>>> - If the user has marked any task a completed by mistake, they will have the opportunity to mark it as incomplete.
>>> - Once the user has clicked the mark as incomplete button the task is then show back at index page and the user is also redirected to index page.

>>Project Details:
>>> - This page shows the deatails of all the tasks in the selected project.
>>> - It also shows to whom the tasks have bee asigned to and the due date.
>>> - User can also mark them ass completed or In progress or mark them as Incompleted, from the details page itself.

>SQL

>> The database has following tables:

>>User:
>>> Stores the details of the users
>>> - First Name
>>> - Last Name
>>> - Username
>>> - hash value of the Password

>>Task:
>>> - Task Id
>>> - Task Name
>>> - Stage Id, which can be co-releted to Inprogress or not started or completed.
>>> - due date
>>> - description.
>>> - Project Id of the project under which the task is made.

>>Project
>>> - Name
>>> - Description
>>> - Start date
>>> - End dated, automatically enterted when the project is completed.

>> User assignment:[links task with user]
>>> - user id
>>> - task id


