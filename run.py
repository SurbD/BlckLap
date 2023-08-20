from flask_login import current_user
from flask import request, redirect, url_for
from flaskapp import create_app, db
from flaskapp.models import User

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User)

if __name__ == "__main__":
    app.run(debug=True, port=5001)