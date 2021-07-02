from flask import Flask, jsonify, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
from werkzeug.utils import secure_filename
import os
from flask_mail import Mail
from werkzeug.utils import redirect


with open('config.json', 'r') as c:
    params = json.load(c)['params']

local_server = params['local_server']

app = Flask(__name__)
# for security in sessions you need to set the secret key
app.secret_key = 'super-secret-key'
app.config['UPLOAD_FOLDER'] = params['upload_location']
app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME = params['gmail-user'],
    MAIL_PASSWORD = params['gmail-password'] 
    
)
mail = Mail(app)
if (local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']

# initialization
db = SQLAlchemy(app)

class Contacts(db.Model):
    '''
        sno, name, phone_num, msg, date, email
    '''
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    phone_num = db.Column(db.String(12),  nullable=False)
    msg = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable=True)
    email = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


class Posts(db.Model):
    '''
        sno, title, slug, content, date
    '''
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    tagline  = db.Column(db.String(80), nullable=False)
    slug = db.Column(db.String(25),  nullable=False)
    content = db.Column(db.String(120), nullable=False)
    img_file = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable=True)

    def __repr__(self):
        return '<User %r>' % self.username

@app.route('/')
def home():
    user = 'Ayushi'
    posts = Posts.query.filter_by().all()[0: params['no_of_posts']]
    return render_template('index.html', params=params, user=user, posts=posts)

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    # if the user is already logged in 
    if 'user' in session and session['user'] == params['admin_user']:
        # provide access
        posts = Posts.query.all()
        return render_template('dashboard.html', params=params, posts=posts)

    if request.method == 'POST':
        # redirect to admin panel
        username = request.form.get('uname')
        userpass =  request.form.get('pass')
        if username == params['admin_user'] and userpass == params['admin_password']:
            # set the session variable 
            session['user'] = username  # basically telling the flask app that this user is logged in 
            posts = Posts.query.all()
            return render_template('dashboard.html', params=params, posts=posts)

    return render_template('login.html', params=params)

@app.route('/logout')
def logout():
    if session['user']:
        session.pop('user')
        return redirect('/dashboard')

@app.route('/delete/<string:sno>', methods=['GET', 'POST'])
def delete(sno):
    if 'user' in session and session['user'] == params['admin_user']:
        print("hit delete")
        # if sno.isnumeric():
        post = Posts.query.get(int(sno))
        db.session.delete(post)
        db.session.commit()
        print("deleted the post")
    return redirect('/dashboard')

@app.route('/edit/<string:sno>', methods=['GET', 'POST'])
def edit(sno):
    if 'user' in session and session['user'] == params['admin_user']:
        if request.method == 'POST':
            title = request.form.get('title')
            tagline = request.form.get('tagline')
            slug = request.form.get('slug')
            content = request.form.get('content')
            img_file = request.form.get('img_file')
            date = datetime.now()

            if sno == '0':
                post = Posts(title=title, tagline=tagline, slug=slug, content=content, img_file=img_file, date=date)
                db.session.add(post)
                db.session.commit()
            else:
                try:
                    int_sno = int(sno)
                    edit_post = Posts.query.filter_by(sno=int_sno).first_or_404(description='There is no post with sno {}'.format(sno))
                    edit_post.title = title
                    edit_post.tagline = tagline
                    edit_post.slug = slug
                    edit_post.content = content
                    edit_post.img_file = img_file
                    edit_post.date = date
                    db.session.commit()
                    return redirect('/edit/'+sno)
                except:
                    print("sno provided was not NAN")
        post = Posts.query.filter_by(sno=sno).first()            
                
        return render_template('edit.html', params=params, post=post)


@app.route('/about')
def about():
    return render_template('about.html', params=params)

@app.route('/uploader', methods=['POST'])
def uploader():
    if request.method == 'POST':
        f = request.files['file1']
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
        return "Uploaded succesfully!"


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        ''' Add entry to the database '''
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        msg = request.form.get('msg')
 
        entry = Contacts(name=name, phone_num=phone, msg=msg, date= datetime.now(), email=email)
        db.session.add(entry)
        db.session.commit()
        mail.send_message('New message from ' + name, 
        sender=email, 
        recipients=[params['gmail-user']],
        body= msg + '\n' + phone
        )


    return render_template('contact.html', params=params)

@app.route('/post/<string:post_slug>', methods=['GET'])
def get_post(post_slug):
    post = Posts.query.filter_by(slug=post_slug).first()
    return render_template('post.html', params=params, post=post)


if __name__ == '__main__':
    app.run(debug=True)


