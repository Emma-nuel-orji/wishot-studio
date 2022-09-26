from flask import Blueprint, render_template, request, flash
from blogapp.models import Post,User
from blogapp.main.form import contactForm
from blogapp import mail
from flask_mail import Message
from flask_login import login_required, current_user

main = Blueprint('main', __name__)


@main.route('/')
@login_required
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=10)
    return render_template('index.html', posts=posts)


@main.route('/about')
@login_required
def about():
    return render_template('about.html')


@main.route('/gallery')
@login_required
def gallery():
    return render_template('gallery.html')


@main.route('/contact', methods=['GET', 'POST'])
@login_required
def contact():
    user = User
    form = contactForm()
    if form.validate_on_submit():
        msg = Message(f'New Message from {current_user.username}', sender=f'{user.email}',
                      recipients=['wishotstudio@gmail.com'])
        msg.body = f"""
           Name :  {form.name.data}

           Email :  {form.contact_email.data}

           Subject :  {form.subject.data}

           Message :  {form.message.data}
           """
        mail.send(msg)
        flash('your message have been sent', 'success')

    return render_template('contact.html', title='contact Form', form=form)
