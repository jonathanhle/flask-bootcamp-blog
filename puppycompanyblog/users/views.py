from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
# connect views to DB object
from puppycompanyblog import db

from puppycompanyblog.models import User, BlogPost
from puppycompanyblog.users.forms import RegistrationForm, LoginForm, UpdateUserForm
from puppycompanyblog.users.picture_handler import add_profile_pic

users = Blueprint('users', __name__)

# -----------------------------------------------------------
# LOGOUT VIEW
# -----------------------------------------------------------


@users.route("/logout")
def logout():
    # from flask_login import of the function
    logout_user()
    return redirect(url_for('core.index'))

# -----------------------------------------------------------
# USER REG
# -----------------------------------------------------------


@users.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    # if the form pis submitted
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)

        db.session.add(user)
        db.session.commit()
        flash('Thanks for registration!')
        return redirect(url_for('users.login'))

    # if it's a brand new form
    return render_template('register.html', form=form)


# -----------------------------------------------------------
# LOGIN
# -----------------------------------------------------------
@users.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user.check_password(form.password.data) and user is not None:

            login_user(user)
            flash('Log in success!')

            # grabs from the current session what the user was actually trying to access
            next = request.args.get('next')

            # if next is was none (they went straight to the login page)
            # or if next wasn't equal to the Homepage
            # go ahead and set next to the Homepage
            if next == None or not next[0] == '/':
                next = url_for('core.index')

            return redirect(next)

    return render_template('login.html', form=form)
