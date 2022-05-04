import time
from flask import Flask, g, request, jsonify, render_template
from datetime import datetime

app = Flask(__name__)
app.config["secret"] = "10"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search')
def search():
    return render_template('search_engine.html')


# our temporary db
users = []


@app.route('/user/', methods=["GET", "POST", "DELETE"])
@app.route('/user/<name>', methods=["GET", "POST", "DELETE"])
def user(name=None):
    if request.method == "GET":
        date = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        # If name is given, lets send decorated response, otherwise return all users till now
        if name:
            return render_template('user.html', user=name, date=date)
        else:
            return render_template('user.html', user=name, users=users)
    elif request.method == "POST" and name:
        # I am just adding name to the in memory db
        users.append(name)
    elif request.method == "DELETE":
        # If the name found in the users, lets delete
        if name in users:
            users.remove(name)
    return jsonify({})


@app.errorhandler(404)
def not_found(e):
    return render_template('error.html', error=e, title="<p>Hello</p>", heading="<h1>Sorry, page not found.</h1>")


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
