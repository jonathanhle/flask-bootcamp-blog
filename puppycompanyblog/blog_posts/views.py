from flask import render_template, url_for, flash, request, redirect, Blueprint
from flask_login import current_user, login_required
from puppycompanyblog import db
from puppycompanyblog.models import BlogPost
from puppycompanyblog.blog_posts.forms import BlogPostForm

blog_posts = Blueprint('blog_posts', __name__)

# -----------------------------------------------------------
# CREATE A BLOG POST
# -----------------------------------------------------------
@blog_posts.route('/create', methods=['GET', 'POST'])
@login_required
def create_post():
    form = BlogPostForm()

    if form.validate_on_submit():

        blog_post = BlogPost(
            title = form.title.data,
            text = form.text.data,
            user_id=current_user.id
        )
    
        db.session.add(blog_post)
        db.session.commit()
        flash('Blog Post Created')
        return redirect(url_for('core.index'))

    return render_template('create_post.html', form=form)


# -----------------------------------------------------------
# VIEW (READ) A BLOG POST
# -----------------------------------------------------------
# < something > in flask/jinja create a variable for the form
# int is just a integer type change - it makes sure the ID is a number not a string
@blog_posts.route('/<int:blog_post_id>', methods=['GET'])
def blog_post(blog_post_id):
    blog_post = BlogPost.query.get_or_404(blog_post_id)
    return render_template('blog_post.html', title=blog_post.title, date=blog_post.date, post=blog_post)

# -----------------------------------------------------------
# UPDATE A BLOG POST
# -----------------------------------------------------------
@blog_posts.route('<int:blog_post_id>/update', methods=['GET', 'POST'])
@login_required
def update(blog_post_id):
    blog_post = BlogPost.query.get_or_404(blog_post_id)

    if blog_post.author != current_user:
        # abort comes with Flask - 403 means forbidden - only let people update their 
        # own blogs
        abort(403)

    form = BlogPostForm()

    if form.validate_on_submit():

        blog_post.title = form.title.data
        blog_post.text = form.text.data
        db.session.commit()
        flash('Blog Post Updated')
        return redirect(url_for('blog_posts.blog_post', blog_post_id = blog_post.id))

    # On first update form view, the fields should have current text and title prefilled
    elif request.method = 'GET':
        form.title.data = blog_post.title
        form.text.data = blog_post.text

    return render_template('create_post.html', title = 'Updating', form=form)

    

# -----------------------------------------------------------
# DELETE A BLOG POST
# this won't have a template, but we'll use a Bootstrap modal
# -----------------------------------------------------------
@blog_posts.route('<int:blog_post_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_post(blog_post_id):

    blog_post = BlogPost.query.get_or_404(blog_post_id)
    if blog_post.author != current_user:
        # abort comes with Flask - 403 means forbidden - only let people update their
        # own blogs
        abort(403)
    
    db.session.delete(blog_post)
    db.session.commit()
    flash('Blog Post Deleted')
    return redirect(url_for('core.index'))