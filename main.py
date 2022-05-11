import os.path

from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config["SECRET_KEY"] = "hard-to-guess-string"
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
moment = Moment(app)


class NameForm(FlaskForm):
    name = StringField("What is your name?", validators=[DataRequired()])
    submit = SubmitField("Submit")


class SearchForm(FlaskForm):
    search = StringField(render_kw={"placeholder": "Search anything"})
    submit = SubmitField("Search")


@app.errorhandler(404)
def not_found(e):
    return render_template('error.html', error=e), 404


@app.route('/', methods=["GET", "POST"])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'))


@app.route('/search', methods=["GET", "POST"])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        if form.search.data:
            search_url = "https://www.google.com/search?q=" + form.search.data.replace(" ", "+")
            return redirect(search_url)
        return redirect(url_for('search'))
    return render_template('search_engine.html', form=form)


if __name__ == '__main__':
    app.run(port=8000, debug=True)
