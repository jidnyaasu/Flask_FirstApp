import os

from flask_migrate import Migrate

from app import create_app, db
from app.models import User, Role

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_contex():
    return dict(db=db, User=User, Role=Role)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
