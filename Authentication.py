from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import os

app= Flask(__name__)
app.config['SECRET_KEY'] = 'b7f8c2e4a1d94e6f9a3c5d7e8f2b4c6a'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
users = {}
tasks = {}

class User(UserMixin):
    def __init__(self,id, username,password_hash):
        self.id=id
        self.username=username
        self.password_hash=password_hash
    @staticmethod
    def get(user_id):
        return users.get(user_id)
        
    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)
        
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)
        
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('tasks_list'))
    return render_template('login.html')
        
@app.route('/register',methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return render_template(url_for('tasks_list'))
            
    if request.method=='POST':
        username=request.form["username"]
        password= request.form["password"]
                 
        if not username or not password:
            flash("Required username and password")
            return render_template('register.html')
                
        for user_id,user_obj in users.items():
            if user_obj.username == username:
                flash("Username already taken.")
                return render_template('register.html')
            
        user_id=str(uuid.uuid4())
        password_hash=generate_password_hash(password)
        new_user=User(user_id,username,password_hash)
        users[user_id]=new_user
        flash("registration Successful!! Please Login")
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return render_template(url_for('tasks_list'))  
    if request.method=='POST':
        username=request.form['username']  
        password=request.form['password']    
        user=None
        for user_id,user_obj in users.items():
            if user_obj.username == username:
                user = user_obj
                break
        if user and user.verify_password(password):
            login_user(user)
            flash("User Logged in Successfully")
            next_page=request.args.get('next')
            return redirect(next_page or url_for('tasks_list'))
        else:
            flash('Invalid Credentials')
    return render_template('login.html')
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You Have Been Logged Out')
    return redirect(url_for('login'))

@app.route('/tasks')
@login_required
def tasks_list():
    user_tasks = tasks.get(current_user.id,[])
    return render_template('tasks.html',tasks=user_tasks)

@app.route('/tasks/add', methods=['POST'])
@login_required
def add_task():
    description=request.form['description']
    if not description:
        flash('Task Description Cannot Be Empty.')
    else:
        task_id=str(uuid.uuid4())
        if current_user.id not in tasks:
            tasks[current_user.id]=[]
            tasks[current_user.id].append({'id':task_id,'description':description})
            flash('Task Added Successfully')
    return redirect(url_for('tasks_list'))

@app.route('/tasks/delete/<task_id>',methods=['POST'])
@login_required
def delete_task(task_id):
    if current_user.id in tasks:
        initial_task_count=len(tasks[current_user.id])
        tasks[current_user.id]=[task for task in tasks[current_user.id] if task['id']!=task_id]
        if len(tasks[current_user.id]) < initial_task_count:
            flash('Task Deleted Successfully!!')
        else:
            flash('Task Not found or you dont have permission to delete this task','error')
    else:
        flash('Task Not found or you dont have permission to delete this task','error')
    return redirect(url_for('tasks_list'))


if __name__=='__main__':
    app.run(debug=True)