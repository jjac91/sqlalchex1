from models import User, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Add users
sam = User(first_name='Sam', last_name='Wise')
kaguya = User(first_name='Kaguya', last_name='Shinomiya',
              image_url='https://cdn.anime-planet.com/characters/primary/kaguya-shinomiya-1-190x266.jpg?t=1625997672')
miyuki = User(first_name='Miyuki', last_name='Shirogane',
              image_url='https://cdn.anime-planet.com/characters/primary/miyuki-shirogane-1-190x266.jpg?t=1625997672')

# Add new objects to session, so they'll persist
db.session.add(sam)
db.session.add(kaguya)
db.session.add(miyuki)

# Commit--otherwise, this never gets saved!
db.session.commit()
