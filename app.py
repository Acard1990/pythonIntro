from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)


@app.route('/appUsers')
def index():
    users = User.query.all()
    return render_template('index.html', users=users)

@app.route('/appUsers', methods=['POST'])
def add_user():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    user = User(first_name=first_name, last_name=last_name, email=email)
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/appUsers/update/<int:id>', methods=['POST'])
def update_user(id):
    user = User.query.get(id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.email = request.form['email']
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/appUsers/delete/<int:id>')
def delete_user(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
