from flask_migrate import Migrate
from datetime import datetime
import bcrypt
from flask import Flask, request, render_template, redirect, session, flash, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'secret_key'  # Replace with a secure key or use environment variables

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///datauserss.db'
db = SQLAlchemy(app)

# Models
class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(1000), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    comments = db.relationship('Comment', backref='blog', lazy=True)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    blogs = db.relationship('Blog', backref='user', lazy=True)
    comments = db.relationship('Comment', backref='user', lazy=True)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    blog_id = db.Column(db.Integer, db.ForeignKey('blog.id'), nullable=False)

# Create database tables
with app.app_context():
    db.create_all()

# Routes
@app.route("/")
def index():
    blogs = Blog.query.order_by(Blog.date_posted.desc()).all()
    return render_template('index.html', blogs=blogs)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered. Please use a different email.', 'danger')
            return redirect(url_for('register'))
        new_user = User(name=name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect('/login')
    return render_template('register.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            session['email'] = user.email
            flash('Login successful!', 'success')
            return redirect('/dashboard')
        else:
            flash('Invalid user credentials.', 'danger')
            return render_template('login.html')
    return render_template('login.html')

@app.route("/logout")
def logout():
    session.pop('email', None)
    flash('You have been logged out.', 'success')
    return redirect('/login')

@app.route("/dashboard", methods=['GET'])
def dashboard():
    if not session.get('email'):
        flash('Please log in to access the dashboard.', 'warning')
        return redirect('/login')
    user = User.query.filter_by(email=session.get('email')).first()
    blogs = Blog.query.filter_by(user_id=user.id).all()
    return render_template('dashboard.html', user=user, blogs=blogs)

@app.route("/post", methods=['POST'])
def post_blog():
    if not session.get('email'):
        flash('Please log in to post a blog.', 'warning')
        return redirect('/login')
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        user = User.query.filter_by(email=session.get('email')).first()
        if user:
            new_blog = Blog(title=title, content=content, user_id=user.id)
            db.session.add(new_blog)
            db.session.commit()
            flash('The blog has been submitted successfully!', 'success')
            return redirect('/dashboard')
    return redirect('/dashboard')

@app.route("/blog/<int:blog_id>")
def view_blog(blog_id):
    blog = Blog.query.get_or_404(blog_id)
    comments = Comment.query.filter_by(blog_id=blog.id).order_by(Comment.date_posted.desc()).all()
    return render_template('blog_detail.html', blog=blog, comments=comments)


@app.route("/blog/<int:blog_id>/comment", methods=['POST'])
def add_comment(blog_id):
    if not session.get('email'):
        flash('Please log in to comment.', 'warning')
        return redirect('/login')
    content = request.form['content']
    user = User.query.filter_by(email=session.get('email')).first()
    if user and content.strip():
        new_comment = Comment(content=content, user_id=user.id, blog_id=blog_id)
        db.session.add(new_comment)
        db.session.commit()
        flash('Comment added successfully!', 'success')
    else:
        flash('Comment cannot be empty.', 'danger')
    return redirect(url_for('view_blog', blog_id=blog_id))

if __name__ == '__main__':
    app.run(debug=True)
