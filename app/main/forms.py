from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class NameForm(FlaskForm):
    name = StringField("What is your name?", validators=[DataRequired()])
    submit = SubmitField("Submit")


class SearchForm(FlaskForm):
    search = StringField(render_kw={"placeholder": "Search anything"})
    submit = SubmitField("Search")
