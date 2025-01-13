# imports
from flask import Flask, render_template, redirect, request
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# My app

app = Flask(__name__)

# Configure Flask-Sass
Scss(app)

# COnfigure SQLAlchemy

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIO"] = False
db = SQLAlchemy(app)

# data class

class MyTask(db.Model):
    id  = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String( 100),nullable=False)
    complete = db.Column(db.Integer,default=0)
    created = db.Column(db.DateTime,default=datetime.utcnow )

    def __str__(self):
        return f"Task {self.id}"

with app.app_context():
    db.create_all()


    
#firstpage
@app.route("/", methods=["POST","GET"])
def index():
    # Add a task
    if request.method == "POST":
        current_task = request.form['content']
        new_task = MyTask(content=current_task)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        
        except Exception as e:
            print(f"ERROR:{e}")
            return f"ERROR {e}"


    # see all task


    else:
        tasks = MyTask.query.order_by(MyTask.created).all()  
        return render_template("index.html",tasks=tasks)




# Delete item
@app.route("/delete/<int:id>")
def delete(id: int):
    delete_task = MyTask.query.get_or_404(id)
    try:
        # Connect to the database and delete the task
        db.session.delete(delete_task)
        db.session.commit()
        return redirect("/")
    except Exception as e:
        print(f"ERROR: {e}")
        return f"ERROR: {e}", 500  # Error response with HTTP 500 status






#edit an item
@app.route("/edit/<int:id>",methods=["GET", "POST"])
def edit(id:int):
    task =  MyTask.query.get_or_404(id)
    if request.method == "POST":
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(f"ERROR: {e}")
            return f"ERROR: {e}"
        
    else:
        return render_template("edit.html",task=task)







if __name__ == "__main__": 
    app.run(debug=True)