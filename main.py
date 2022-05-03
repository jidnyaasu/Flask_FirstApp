import time
from flask import Flask, g, request, jsonify, render_template
from routes import test

app = Flask(__name__)
app.config["secret"] = "10"


@app.route('/')
def index():
    return '<h1>Hello World!</h1>'


@app.route('/search')
def search():
    return render_template('search_engine.html')


# our temporary db
users = []


@app.route('/user/', methods=["GET", "POST", "DELETE"])
@app.route('/user/<name>', methods=["GET", "POST", "DELETE"])
def user(name=None):
    if request.method == "GET":
        # If name is given, lets send decorated response, otherwise return all users till now
        if name:
            return test(name)
        else:
            return jsonify(users)
    elif request.method == "POST" and name:
        # I am just adding name to the in memory db
        users.append(name)
    elif request.method == "DELETE":
        # If the name found in the users, lets delete
        if name in users:
            users.remove(name)
    return jsonify({})


# calculator app
@app.route('/calc/')
@app.route('/calc/<expression>')
def calc(expression=None):
    if expression is None:
        return f'<p><b>Nothing to calculate</b></p>'
    if '+' in expression:
        expression_list = expression.split("+")
        answer = int(expression_list[0]) + int(expression_list[1])
        return f"<p>{expression} = {answer}</p>"
    if '-' in expression:
        expression_list = expression.split("-")
        answer = int(expression_list[0]) - int(expression_list[1])
        return f"<p>{expression} = {answer}</p>"
    if '*' in expression:
        expression_list = expression.split("*")
        answer = int(expression_list[0]) * int(expression_list[1])
        return f"<p>{expression} = {answer}</p>"
    if '%' in expression:
        expression_list = expression.split("%")
        answer = int(expression_list[0]) / int(expression_list[1])
        return f"<p>{expression} = {answer}</p>"


@app.errorhandler(404)
def not_found(e):
    return render_template('error.html')


@app.before_request
def before_request():
    # in the g object lets store the current time
    # later in after request, lets calculate total time
    g.request_start_time = time.time()
    g.req_time = lambda: "%.5fs" % (time.time() - g.request_start_time)


@app.after_request
def after_request(response):
    """
    print the total req time.
    :param response:
    :return:
    """
    print(g.req_time())
    return response


if __name__ == '__main__':
    app.run(port=8000, debug=True)
