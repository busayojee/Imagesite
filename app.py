from datetime import datetime
from flask import Flask, render_template, request, flash, redirect, url_for, session, abort, g
import os
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads/'
app.secret_key = 'damiportfolio'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dami.db'
db =  SQLAlchemy(app)
class Img(db.Model):
    id = db.Column(db.Integer, nullable = False, primary_key = True)
    filename = db.Column(db.String(20))
    name = db.Column(db.String(20), nullable=False, default = "N/A")
    caption = db.Column(db.Text, nullable = False, default = "No caption")
    date_added = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    comment = db.relationship('Comment')
class Comment(db.Model):
    com_id  = db.Column(db.Integer, nullable=False, primary_key = True)
    com_name = db.Column(db.String(30), nullable=False, default = "N/A")
    email = db.Column(db.String(30), nullable=False, default = "N/A")
    com_comment = db.Column(db.Text, nullable = False, default ="No comment")
    come_date = db.Column(db.DateTime, nullable=False, default = datetime.utcnow)
    id  = db.Column(db.Integer, db.ForeignKey('img.id'))

# comments = Comment.query.all() 
# for com in comments:
#     # db.session.delete(com)
#     # db.session.commit()
#     print(com)
# db.create_all()

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'mp4'])
login_db = {"busayo":"busayo", "damilola":"victoria"}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@app.route('/', methods = ['GET', 'POST'])
def home():
    images = Img.query.order_by(desc(Img.date_added)).all()
    if request.method == 'POST':
        session.pop('name', None)
        username = request.form['username']
        password = request.form['password']
        session['name'] = username
        session['pwd'] = password
        if username not in login_db:
            session.pop('name', None)
            return render_template('index.html', images = images)
        else:
            if login_db[username]!= password:
                session.pop('name', None)
                return render_template('index.html', images = images)
            else:
                return redirect('/main')
    else:
        if 'name' and 'pwd' in session:
            return redirect(url_for('main'))
        return render_template("index.html", images = images)
@app.route('/main')
def main():
    images = Img.query.order_by(desc(Img.date_added)).all()
    if g.name:
        return render_template('main.html', images = images)
    return render_template("index.html", images = images)
@app.before_request
def before_request():
    g.name = None
    if 'name' in session:
        g.name = session['name']
@app.route('/logout')
def logout():
    if 'name' and 'pwd' in session:
        session.pop('name', None)
        session.pop('pwd', None)
    return redirect('/')
@app.route('/about')
def about():
    if g.name:
        return render_template('aboutn.html')
    return render_template("about.html")
@app.route('/upload', methods = ['GET','POST'])
def upload():
    images = Img.query.order_by(desc(Img.date_added)).all()
    if g.name:
        if request.method == 'POST':
            name = request.form['name']
            caption =request.form['caption']
            if 'file' not in request.files:
                flash('No file selected')
                return redirect(request.url)
            file = request.files['file']
            if file.filename == '':
                flash('No image selected for uploading')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                flash('image successfully uploaded')
                new_file = Img(filename = filename, name = name, caption = caption)
                db.session.add(new_file)
                db.session.commit()
                return render_template('img.html', images = images)
            else:
                flash("Not allowed image type")
                return redirect(request.url)
        else:
            # path = 'static/uploads/'
            # uploads = sorted(os.listdir(path), key= lambda x: os.path.getctime(path+x))
            # print(uploads)
            # uploads = ('uploads/' + file for file in uploads)
            # uploads.reverse()
            return render_template('img.html', images = images)
            # return redirect(request.url)
    return render_template("index.html", images = images)
@app.route('/art/<int:id>')
def art(id):
    arts = Img.query.filter(Img.id == id).all()
    comments = Comment.query.filter(Comment.id == id).all()
    comments = len(comments)
    if g.name:
        if arts:
            return render_template("art.html", arts = arts, comments = comments)
        else:
            abort(404)
    else:
        if arts:
            return render_template('arts.html', arts = arts, comments = comments)
        else:
            abort(404)
@app.route('/delete/<int:id>')
def delete(id):
    arts = Img.query.get_or_404(id)
    coms = Comment.query.filter(Comment.id == id).all()
    if g.name:
        if arts:
            if os.path.exists('static/uploads/' + arts.filename):
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], arts.filename))
            db.session.delete(arts)
            db.session.commit()
            for com in coms:
                db.session.delete(com)
                db.session.commit()
            return redirect('/')
        else:
            abort(404)
    else:
        abort(404)
@app.route("/art/comment/<int:id>", methods = ['GET', 'POST'])
def comment(id):
    arts = Img.query.get_or_404(id)
    comments = Comment.query.filter(Comment.id == id).order_by(desc(Comment.come_date)).all()
    if request.method == 'POST':
        name = request.form['nickname']
        email = request.form['email']
        comment = request.form['comment']
        new_comment = Comment(com_name= name, email = email, com_comment = comment, id = id)
        db.session.add(new_comment)
        db.session.commit()
        return redirect("/")
    else:
        if g.name:
            return render_template('comment.html', comments = comments, arts = arts)
        return render_template('commentmain.html', comments = comments, arts = arts)

@app.route("/comment/delete/<int:id>")
def delete_comment(id):
    com = Comment.query.get_or_404(id)
    if g.name:
        if com:
            db.session.delete(com)
            db.session.commit()
            return redirect(url_for("main"))
        else:
            abort(404)
    else:
        abort(404)

if __name__ ==  "__main__":
    app.run(debug=True, host="0.0.0.0", port=80)