"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User, Post, Tag, PostTag
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = "oh-so-secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route("/")
def root():
    """redirects to page with list of users"""

    return redirect("/users")


@app.route("/users")
def list_users():
    """List all users on page"""

    users = User.query.all()
    return render_template("users.html", users=users)


@app.route("/users/new", methods=["GET"])
def new_form():
    """returns a form to create a new user"""
    return render_template("form.html")


@app.route("/users/new", methods=["POST"])
def add_user():
    """handles submission of a form to create a new user"""
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]
    image_url = image_url if image_url else None

    user = User(first_name=first_name,
                last_name=last_name, image_url=image_url)
    db.session.add(user)
    db.session.commit()
    return redirect("/users")


@app.route("/users/<int:user_id>")
def show_user(user_id):
    """Show info on a single user."""

    user = User.query.get_or_404(user_id)
    return render_template("details.html", user=user)


@app.route("/users/<int:user_id>/edit")
def edit_user(user_id):
    """Returns a form for a user to edit their profile"""
    user = User.query.get_or_404(user_id)
    return render_template("edit.html", user=user)


@app.route("/users/<int:user_id>/edit", methods=["POST"])
def handle_edit_user(user_id):
    """Handles a form to edit existing user"""

    user = User.query.get_or_404(user_id)
    user.first_name = request.form["first_name"]
    user.last_name = request.form["last_name"]
    user.image_url = request.form["image_url"]

    db.session.add(user)
    db.session.commit()
    return redirect("/users")


@app.route('/users/<int:user_id>/delete', methods=["POST"])
def del_user(user_id):
    """Handles form for deleting user"""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect("/users")


###########Posts###############

@app.route("/users/<int:user_id>/posts/new", methods=["GET"])
def new_post_form(user_id):
    """returns a form to create a new post"""
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template("post_form.html", user=user, tags=tags)


@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def new_post(user_id):
    """handles sumbmission of new post form"""

    title = request.form["title"]
    content = request.form["content"]
    user = User.query.get_or_404(user_id)
    tag_ids = [int(num) for num in request.form.getlist("tag")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    post = Post(title=title,
                content=content, user=user, tag=tags)
    db.session.add(post)
    db.session.commit()
    return redirect(f"/users/{user_id}")


@app.route("/posts/<int:post_id>")
def show_post(post_id):
    """shows a page with a post"""

    post = Post.query.get_or_404(post_id)
    return render_template("post.html", post=post)


@app.route("/posts/<int:post_id>/edit")
def edit_post(post_id):
    """Returns a form for a user to edit their post"""
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    return render_template("edit_post.html", post=post, tags=tags)


@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def handle_edit_post(post_id):
    """handles a form to edit existing post"""

    post = Post.query.get_or_404(post_id)
    post.title = request.form["title"]
    post.content = request.form["content"]
    tag_ids = [int(num) for num in request.form.getlist("tag")]
    post.tag = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    db.session.add(post)
    db.session.commit()
    return redirect(f"/posts/{post_id}")


@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    """Handles request for deleting a post"""
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(f"/users/{post.user_id}")


########Tags#######

@app.route("/tags")
def list_tags():
    """List all tags on a page"""

    tags = Tag.query.all()
    return render_template("tags.html", tags=tags)


@app.route("/tags/<int:tag_id>")
def show_tag(tag_id):
    """Show info on a single user."""

    tag = Tag.query.get_or_404(tag_id)
    return render_template("tag.html", tag=tag)


@app.route("/tags/new", methods=["GET"])
def new_tag():
    """returns a form to create a new tag"""
    return render_template("tag_form.html")


@app.route("/tags/new", methods=["POST"])
def add_tag():
    """handles submission of a form to create a new tag"""
    name = request.form["tag_name"]

    tag = Tag(name=name)
    db.session.add(tag)
    db.session.commit()
    return redirect("/tags")


@app.route("/tags/<int:tag_id>/edit")
def edit_tag(tag_id):
    """returns a form to edit a tag"""
    tag = Tag.query.get_or_404(tag_id)
    return render_template("edit_tag.html", tag=tag)


@app.route("/tags/<int:tag_id>/edit", methods=["POST"])
def handle_edit_tag(tag_id):
    """handles submission of a form to edit a tag"""
    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form["tag_name"]
    db.session.add(tag)
    db.session.commit()
    return redirect("/tags")


@app.route("/tags/<int:tag_id>/delete", methods=["POST"])
def delete_tag(tag_id):
    """Handles request for deleting a tag"""
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    return redirect("/tags")
