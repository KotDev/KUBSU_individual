from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, login_required, logout_user, current_user
from flask_mail import Mail

from config import conf
from summer_tasks.task_4.froms.forms import RegistrationForm, SearchForm, LoginForm,  SendMessageForm, AddUserForm
from database import session, Base, engine
from summer_tasks.task_4.app.model import User
from summer_tasks.task_4.app.control import ProfileUserOptions, IdentificationUser, AdminUserOptions

app = Flask(__name__)

app.config['SECRET_KEY'] = conf['SECRET_KEY']
app.config['MAIL_SERVER'] = conf['MAIL_SERVER']
app.config['MAIL_PORT'] = conf['MAIL_PORT']
app.config['MAIL_USE_TLS'] = conf['MAIL_USE_TLS']
app.config['MAIL_USERNAME'] = conf['MAIL_USERNAME']
app.config['MAIL_DEFAULT_SENDER'] = conf['MAIL_DEFAULT_SENDER']
app.config['MAIL_PASSWORD'] = conf['MAIL_PASSWORD']

login_manager = LoginManager(app)
mail = Mail(app)


@login_manager.user_loader
def load_user(user_id):
    return session.query(User).filter(User.id == user_id).first()


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('authentication_vew'))


@app.route("/authentication", methods=["GET", "POST"])
def authentication_vew():
    form = LoginForm()
    aunt = IdentificationUser.login_user(session, form)
    if aunt:
        return redirect(url_for('profile_user'))
    return render_template("login.html", form=form, user=current_user)


@app.route("/register", methods=["GET", "POST"])
def register_view():
    form = RegistrationForm()
    reg = IdentificationUser.register_user(session, form)
    if reg:
        return redirect(url_for("profile_user"))
    return render_template("register.html", form=form, user=current_user)


@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("authentication_vew"))


@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile_user():
    form = ProfileUserOptions.edit_profile(session, current_user.id)
    return render_template("profile.html", form=form, user=current_user)


@app.route("/search", methods=["GET", "POST"])
@login_required
def search_user():
    form = SearchForm()
    context_data = {"users_list": ProfileUserOptions.search_profile(form, session)}
    return render_template("search_list.html", **context_data, form=form, user=current_user)


@app.route("/user_profile/<int:user_id>", methods=["GET", "POST"])
@login_required
def user_profile(user_id):
    context_data = ProfileUserOptions.see_profile(session, user_id)
    return render_template("user_profile.html", **context_data)


@app.route("/user_profile/<int:user_id>/edit", methods=["GET", "POST"])
@login_required
def edit_profile_user(user_id):
    context_data, form = AdminUserOptions.edit_profile_user(session, user_id)
    return render_template("edit_profile_user.html", **context_data, form=form, user=current_user)


@app.route("/user_profile/<int:user_id>/delete", methods=["GET", "POST"])
@login_required
def delete_user(user_id):
    delete, user = AdminUserOptions.delete_user(user_id, session)
    if delete:
        return redirect(url_for("search_user"))
    return render_template("delete_user.html", user=user)


@app.route("/add_user", methods=["GET", "POST"])
@login_required
def add_user():
    form = AddUserForm()
    if AdminUserOptions.add_user(session, form):
        return redirect(url_for("search_user"))
    return render_template("add_user.html", form=form, user=current_user)


@app.route("/user_profile/<int:user_id>/message", methods=["GET", "POST"])
@login_required
def send_message_vew(user_id):
    form = SendMessageForm()
    user_recipient = session.query(User).filter(User.id == user_id).first()
    msg = AdminUserOptions.send_message(form, user_recipient)
    if msg is not None:
        mail.send(msg)
        return redirect(url_for("search_user"))
    else:
        return render_template("send_email.html", form=form,  user=current_user,
                               user_recipient=user_recipient)


@app.route("/")
@login_required
def index():
    return render_template("base.html", user=current_user)

