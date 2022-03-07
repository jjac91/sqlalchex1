from models import User, db, Post, Tag, PostTag
from app import app

# Create all tables
db.drop_all()
db.create_all()

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

# Add posts
post1 = Post(title="test1", content="test1", user_id=1)
post2 = Post(title="test2", content="test2", user_id=2)
post3 = Post(title="test3", content="test3", user_id=3)

db.session.add(post1)
db.session.add(post2)
db.session.add(post3)

db.session.commit()

# Add Tags
tag1 = Tag(name="happy")
tag2 = Tag(name="sad")
tag3 = Tag(name="excited")

db.session.add(tag1)
db.session.add(tag2)
db.session.add(tag3)

db.session.commit()
# Add PostTags

posttag1 = PostTag(post_id=2, tag_id=1)
posttag2 = PostTag(post_id=2, tag_id=2)
posttag3 = PostTag(post_id=2, tag_id=3)

db.session.add(posttag1)
db.session.add(posttag2)
db.session.add(posttag3)

db.session.commit()
