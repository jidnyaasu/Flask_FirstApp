from flask import render_template, session, redirect, url_for, current_app

from . import main
from .forms import NameForm, SearchForm
from .. import db
from ..email import send_email
from ..models import User


@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        username = form.name.data.capitalize()
        user = User.query.filter_by(username=username).first()
        if user is None:
            user = User(username=username, role_id=2)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
            if current_app.config["SOCIAL_APP_ADMIN"]:
                send_email(current_app.config["SOCIAL_APP_ADMIN"], 'New User', 'mail/new_user', user=user)
        else:
            session['known'] = True
        session['name'] = username
        form.name.data = ''
        return redirect(url_for('.index'))
    return render_template('index.html', form=form, name=session.get('name'),
                           known=session.get('known', False))


@main.route('/search', methods=["GET", "POST"])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        if "social" in (form.search.data.lower().strip().split(" ")) \
                and "app" in (form.search.data.lower().strip().split(" ")):
            return redirect(url_for('.index'))
        elif form.search.data:
            search_url = "https://www.google.com/search?q=" + form.search.data.replace(" ", "+")
            return redirect(search_url)
        return redirect(url_for('.search'))
    return render_template('search_engine.html', form=form)
