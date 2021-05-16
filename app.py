from flask import Flask, url_for, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# url_for generates URL for the API's endpoint.
# render_template allows to work with html templates and use blocks.
# request for creating request objects.
# redirect for redirecting the client to the target location.

# SQLAlchemy for SQL creating a simple DB.

# datetime for using date time data type.

# Declaring Flask, DB and config.
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


# Building the DB
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())
    comments = db.Column(db.String(200), nullable=False)


def __repr__(self):
    return '<Task %r>' % self.id


# Create task app
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        task_comments = request.form['comments']
        new_task = Todo(content=task_content, comments=task_comments)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'Error while creating task'

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template("index.html", tasks=tasks)


# Delete task app
@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'Error while deleting task'


# Modify task app
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']
        task.comments = request.form['comment']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'Error while updating task'

    else:
        return render_template('update.html', task=task)


if __name__ == "__main__":
    app.run(debug=True)
