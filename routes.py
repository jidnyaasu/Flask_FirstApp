
from flask import current_app as app, g, request


def test(name):
    info = f'<p>Hello, {name} {app.config["secret"]} {request.headers.get("user-agent")} {g.request_start_time}!</p>'
    return info