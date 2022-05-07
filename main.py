from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, HiddenField, RadioField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config["SECRET_KEY"] = "hard to guess string"

bootstrap = Bootstrap(app)
moment = Moment(app)


class NameForm(FlaskForm):
    name = StringField("What is your name?", validators=[DataRequired()])
    password = PasswordField("Enter your password")
    hidden = HiddenField("Text entered here will be hidden")
    gender = RadioField("Male", "Female")
    submit = SubmitField("Submit")


@app.errorhandler(404)
def not_found(e):
    return render_template('error.html', error=e, title="404 Not Found", heading="<h1>Sorry, page not found.</h1>"), 404


@app.route('/', methods=["GET", "POST"])
def index():
    name = None
    return render_template('index.html')


if __name__ == '__main__':
    app.run(port=8000, debug=True)
