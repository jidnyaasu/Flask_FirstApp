import time


def test(name):
    info = f"<p>Hello, {name}! It's {time.time()} right now.</p>"
    return info
