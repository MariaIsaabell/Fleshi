from appfleshi import database, app
from appfleshi.models import Photo, User

with app.app_context():
    database.create_all()

