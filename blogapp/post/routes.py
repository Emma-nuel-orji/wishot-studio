from flask import Blueprint, request, render_template, url_for, flash, redirect, abort
from flask_login import login_required, current_user
from blogapp import db
from blogapp.models import Post
from blogapp.post.forms import PostForm


posts = Blueprint('posts', __name__)


@posts.route('/post', methods=['POST', 'GET'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('your Post Has Been Created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('control.html', title='New Post', legend='New post', form=form)


@posts.route('/post-<int:post_id>', methods=['POST', 'GET'])
def single(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('single-post.html', title=post.title, post=post)


@posts.route('/post-<int:post_id>-update', methods=['POST', 'GET'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash("Your Post Has Been Updated!", "success")
        return redirect(url_for('posts.single', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('control.html', title='Update Post', legend='update post', form=form)


@posts.route('/post-<int:post_id>-delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash("Your Post Has Been Deleted!", "success")
    return redirect(url_for('main.home'))

