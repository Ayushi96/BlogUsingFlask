from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

local_server = True

with open('config.json', 'r') as c:
    params = json.load(c)['params']

app = Flask(__name__)

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

@app.route('/')
def home():
    user = 'Ayushi'
    return render_template('index.html', params=params)

@app.route('/about')
def about():
    return render_template('about.html', params=params)
    
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


    return render_template('contact.html', params=params)



if __name__ == '__main__':
    app.run(debug=True)


