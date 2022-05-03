from datetime import datetime


def test(name):
    info = f"<p>Hello, {name}! It's {datetime.now().strftime('%d-%m-%Y %H:%M:%S')} right now.</p>"
    return info
