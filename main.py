import os
from threading import Thread

from flask import Flask, render_template, session, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_mail import Mail, Message
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv('SECRET_KEY')
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["MAIL_SERVER"] = 'smtp.googlemail.com'
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.getenv('MAIL_USERNAME')
app.config["MAIL_PASSWORD"] = os.getenv('MAIL_PASSWORD')
app.config["MAIL_SUBJECT_PREFIX"] = '[Social App]'
app.config["SOCIAL_APP_MAIL_SENDER"] = f'Social App Admin {app.config["MAIL_USERNAME"]}'
app.config["SOCIAL_APP_ADMIN"] = os.getenv("SOCIAL_APP_ADMIN")

db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
migrate = Migrate(app, db)
mail = Mail(app)


class NameForm(FlaskForm):
    name = StringField("What is your name?", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    submit = SubmitField("Submit")


class SearchForm(FlaskForm):
    search = StringField(render_kw={"placeholder": "Search anything"})
    submit = SubmitField("Search")


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return f'<Role {self.name}'


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password = db.Column(db.String(64))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return f'<User {self.username}'


@app.shell_context_processor
def make_shell_contex():
    return dict(db=db, User=User, Role=Role)


@app.errorhandler(404)
def not_found(e):
    return render_template('error.html', error=e), 404


@app.route('/', methods=["GET", "POST"])
def index():
    form = NameForm()
    if form.validate_on_submit():
        username = form.name.data.capitalize()
        user = User.query.filter_by(username=username).first()
        if user is None:
            user = User(username=username, role_id=2, password=form.password.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
            if app.config["SOCIAL_APP_ADMIN"]:
                send_email(app.config["SOCIAL_APP_ADMIN"], 'New User', 'mail/new_user', user=user)
        elif user.password is None:
            user.password = form.password.data
            db.session.commit()
            session['known'] = True
        else:
            session['known'] = True
        session['name'] = username
        session['password'] = form.password.data
        form.name.data = ''
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'),
                           password=session.get('password'), known=session.get('known', False))


@app.route('/search', methods=["GET", "POST"])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        if "social" in (form.search.data.lower().strip().split(" ")) \
                and "app" in (form.search.data.lower().strip().split(" ")):
            return redirect(url_for('index'))
        elif form.search.data:
            search_url = "https://www.google.com/search?q=" + form.search.data.replace(" ", "+")
            return redirect(search_url)
        return redirect(url_for('search'))
    return render_template('search_engine.html', form=form)


def send_async_email(msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, template, **kwargs):
    msg = Message(app.config["MAIL_SUBJECT_PREFIX"] + " " + subject,
                  sender=app.config["SOCIAL_APP_MAIL_SENDER"], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[msg])
    thr.start()
    return thr


db.create_all()

if __name__ == '__main__':
    app.run(port=8000, debug=True)
