import datetime


def test(name):
    info = f"<p>Hello, {name}! It's {datetime.datetime.now()} right now.</p>"
    return info
