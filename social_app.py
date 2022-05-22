import os

from app import create_app, db
from app.models import User, Role
from flask_migrate import Migrate


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_contex():
    return dict(db=db, User=User, Role=Role)


db.create_all()

if __name__ == '__main__':
    app.run(port=8000, debug=True)
