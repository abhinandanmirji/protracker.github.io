import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from flask import url_for


from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///test.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    user = db.execute(
        "SELECT first_name, last_name FROM user WHERE user_id = :user_id",
        user_id=session["user_id"],
    )

    tasks = db.execute(
        """
        SELECT task.task_id AS task_id, task.task_name, description, due_date,
        task.stage_id AS task_stage_id, stage.stage_name AS stage_name
    FROM task
    INNER JOIN assignment ON task.task_id = assignment.task_id
    INNER JOIN stage ON task.stage_id = stage.stage_id  -- Use task.stage_id here
    WHERE user_id = :user_id AND task.stage_id IN (SELECT stage_id FROM stage WHERE stage_name = 'In Progress' OR stage_name = 'Not Started')
    ORDER BY stage_name DESC, due_date ASC

        """,


        user_id=session["user_id"],
    )

    return render_template(
        "index.html",
        user=user,
        tasks=tasks,
    )


@app.route("/history")
@login_required
def history():
    user_id = session["user_id"]
    completed_tasks = db.execute(
        """
        SELECT task.task_name, task.description, task.completion_date, task.task_id AS task_id
        FROM task
        INNER JOIN assignment ON task.task_id = assignment.task_id
        WHERE user_id = :user_id AND stage_id = (SELECT stage_id FROM stage WHERE stage_name = 'Completed')
        """,
        user_id=user_id,
    )
    return render_template("history.html", completed_tasks=completed_tasks)


@app.route("/mark_incomplete/<int:task_id>", methods=["POST"])
def mark_incomplete(task_id):
    # Update task stage to "In Progress" or other relevant stage (replace with your logic)
    db.execute(
        """
        UPDATE task SET stage_id = (SELECT stage_id FROM stage WHERE stage_name = 'In Progress')
        WHERE task_id = :task_id
        """,
        task_id=task_id,
    )
    # Flash message or redirect (optional)
    flash('Task marked as incomplete!', 'success')
    return redirect(url_for('history'))


@app.route("/mark_complete/<int:task_id>", methods=["POST"])
def mark_complete(task_id):
    # Update task stage and set completion date
    db.execute(
        """
        UPDATE task SET stage_id = (SELECT stage_id FROM stage WHERE stage_name = 'Completed'),
                       completion_date = CURRENT_DATE
        WHERE task_id = :task_id
        """,
        task_id=task_id,
    )
    flash('Task marked as completed!', 'success')
    return redirect(url_for('index'))  # Redirect back to main page


@app.route("/mark_in_progress/<int:task_id>", methods=["POST"])
def mark_in_progress(task_id):
    # Update task stage to "In Progress" or other relevant stage (replace with your logic)
    db.execute(
        "UPDATE task SET stage_id = (SELECT stage_id FROM stage WHERE stage_name = 'In Progress') WHERE task_id = :task_id",
        task_id=task_id,
    )
    # Flash message or redirect (optional)
    flash('Task marked as in progress!', 'success')
    return redirect(url_for('index'))  # Redirect back to main page


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM user WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["user_id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        if not request.form.get("username"):
            return apology("must provide username", 400)
        if not request.form.get("password"):
            return apology("must provide password", 400)

        if not request.form.get("first_name"):
            return apology("must provide Name", 400)

        elif not request.form.get("last_name"):
            return apology("must provide last Name", 400)
        elif not request.form.get("confirmation"):
            return apology("re enter password", 400)
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("Password does not match")
        rows = db.execute(
            "SELECT * FROM user WHERE username = ?", request.form.get("username")
        )
        if len(rows) != 0:
            return apology("username already exits", 400)
        db.execute(
            "INSERT INTO user (username, first_name, last_name, hash) VALUES (?, ?, ?, ?)",
            request.form.get("username"), request.form.get("first_name"), request.form.get("last_name"),
            generate_password_hash(request.form.get("password")),
        )
        rows = db.execute(
            "SELECT * FROM user WHERE username = ?", request.form.get("username")
        )
        session["user_id"] = rows[0]["user_id"]
        # Redirect user to home page
        return redirect("/")

        # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/create", methods=["GET", "POST"])
@login_required
def create():
    if request.method == "POST":
        if not request.form.get("title"):
            return apology("must provide title", 400)
        if not request.form.get("description"):
            return apology("must provide description", 400)

        # Insert project data
        db.execute(
            "INSERT INTO project (project_name, description, start_date, stage_id) VALUES (?, ?, ?, ?)",
            request.form.get("title"),
            request.form.get("description"),
            request.form.get("start_date"),
            4
        )

        return redirect(url_for("project"))
    else:
        return render_template("create.html")


@app.route("/project")
@login_required
def project():

    projects = db.execute(
        """

        SELECT  project.project_id, project.project_name, project.description, project.start_date, project.end_date, stage.stage_name
        FROM project
        JOIN stage ON project.stage_id = stage.stage_id
        ORDER BY end_date ASC

        """,
    )

    return render_template(
        "project.html",

        projects=projects,
    )


@app.route("/project_details/<int:project_id>", methods=["GET", "POST"])
@login_required
def project_details(project_id):

    tasks = db.execute(
        """


         SELECT task.task_id AS task_id, task.task_name, description, due_date,
        task.stage_id AS task_stage_id, stage.stage_name AS stage_name, user.username AS username
    FROM task
    INNER JOIN assignment ON task.task_id = assignment.task_id
    INNER JOIN stage ON task.stage_id = stage.stage_id
    JOIN user ON assignment.user_id = user.user_id
    WHERE project_id = ?
    ORDER BY stage_name DESC, due_date ASC

        """,


        project_id,
    )

    return render_template(
        "project_details.html",
        tasks=tasks,
    )


@app.route("/mark_incomplete_p/<int:project_id>", methods=["POST"])
def mark_incomplete_p(project_id):
    # Update task stage to "In Progress" or other relevant stage (replace with your logic)
    db.execute(
        """
        UPDATE project SET stage_id = (SELECT stage_id FROM stage WHERE stage_name = 'In Progress')
        WHERE project_id = :project_id
        """,
        project_id=project_id,
    )
    # Flash message or redirect (optional)
    flash('Task marked as incomplete!', 'success')
    return redirect(url_for('project'))


@app.route("/mark_complete_p/<int:project_id>", methods=["POST"])
def mark_complete_p(project_id):
    # Update task stage and set completion date
    db.execute(
        """
        UPDATE project SET stage_id = (SELECT stage_id FROM stage WHERE stage_name = 'Completed'),
                       end_date = CURRENT_DATE
        WHERE project_id = :project_id
        """,
        project_id=project_id,
    )
    flash('Task marked as completed!', 'success')
    return redirect(url_for('project'))  # Redirect back to main page


@app.route("/mark_in_progress_p/<int:project_id>", methods=["POST"])
def mark_in_progress_p(project_id):
    # Update task stage to "In Progress" or other relevant stage (replace with your logic)
    db.execute(
        "UPDATE project SET stage_id = (SELECT stage_id FROM stage WHERE stage_name = 'In Progress') WHERE project_id = :project_id",
        project_id=project_id,
    )
    # Flash message or redirect (optional)
    flash('Task marked as in progress!', 'success')
    return render_template("project.html")  # Redirect back to main page


@app.route("/task", methods=["GET", "POST"])
@login_required
def task():
    if request.method == "POST":
        if not request.form.get("task_name"):
            return apology("must provide title", 400)
        if not request.form.get("description"):
            return apology("must provide description", 400)

        # Insert project data
        db.execute(
            "INSERT INTO task (task_name, description, due_date, project_id, stage_id) VALUES (?, ?, ?, ?, ?)",
            request.form.get("task_name"),
            request.form.get("description"),
            request.form.get("due_date"),
            request.form.get("project_id"),
            4
        )
        project_id = request.form.get("project_id")
        print(project_id)

        id = db.execute(
            "SELECT task_id FROM task WHERE task_name = ? AND project_id = ?", request.form.get(
                "task_name"), request.form.get("project_id")
        )
        user_id = db.execute(
            " SELECT user_id FROM user WHERE username = ?", request.form.get("username")
        )
        print(user_id)
        userid = user_id[0]['user_id']
        task_id = id[0]['task_id']

        db.execute(
            "INSERT INTO assignment (user_id, task_id) VALUES (?, ?)", userid, task_id
        )

        return redirect(url_for("project"))
    else:
        projects = db.execute(
            """

        SELECT project_id, project_name FROM project
        ORDER BY end_date ASC

        """,
        )
        users = db.execute(
            """

        SELECT user_id, username FROM user

        """,
        )
        return render_template("task.html", projects=projects, users=users)

if __name__ == "__main__":
    app.run()
