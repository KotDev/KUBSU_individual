from flask import redirect, url_for, request, flash
from flask_login import login_user, current_user
from sqlalchemy import or_
from werkzeug import security
from flask_mail import Message
from summer_tasks.task_4.froms.forms import EditProfileForm
from summer_tasks.task_4.app.model import User


class BaseUserOptions:

    @staticmethod
    def edit_user(url_redirect, user_id, form, session, value_url):
        if request.method == "POST":
            if form.validate_on_submit():
                form.phone_number.data = form.phone_number.data.replace("+7", "8")
                data = form.data
                data.pop("csrf_token")
                data.pop("submit")
                data["first_name"] = data["first_name"].capitalize()
                data["second_name"] = data["second_name"].capitalize()
                data["surname"] = data["surname"].capitalize()
                if len(session.query(User).filter(or_(User.login == data["login"], User.email_name == data["email_name"],
                                                      User.phone_number == data["phone_number"])).all()) == 1:
                    session.query(User).filter(User.id == user_id).update(data)
                    session.commit()
                    form.phone_number.data = (session.query(User).filter(User.id == user_id).first().
                                              phone_number.replace("8", "+7", 1))
                    session.close()
                    return redirect(url_for(url_redirect, **value_url))
                session.close()
                form.phone_number.data = form.phone_number.data.replace("8", "+7", 1)
                flash("Такой пользователь уже существует")

    @staticmethod
    def create_user(form, session):
        user = None
        if form.validate_on_submit():
            data = form.data
            data["first_name"] = data["first_name"].capitalize()
            data["second_name"] = data["second_name"].capitalize()
            data["surname"] = data["surname"].capitalize()
            data['phone_number'] = data['phone_number'].replace("+7", "8")
            if session.query(User).filter(or_(User.login == data['login'],
                                          User.email_name == data['email_name'],
                                          User.phone_number == data['phone_number'])).first() is not None:
                session.close()
                flash("Такой пользователь уже существует")
            else:
                data['password'] = security.generate_password_hash(password=data['password'])
                data.pop('confirm')
                data.pop('submit')
                data.pop('csrf_token')
                user = User(**data)
                session.add(user)
                session.commit()
        return user


class IdentificationUser(BaseUserOptions):

    @staticmethod
    def register_user(session, form):
        user = BaseUserOptions.create_user(form, session)
        if user is not None:
            login_user(user)
            return True
        return False

    @staticmethod
    def login_user(session, form):
        if form.validate_on_submit():
            password = form.password.data
            login = form.login.data
            user = session.query(User).filter(User.login == login).first()
            session.close()
            if user is not None:
                if security.check_password_hash(user.password, password):
                    login_user(user)
                    return True
        flash("Неверный логин или пароль")
        return False


class ProfileUserOptions(BaseUserOptions):

    @staticmethod
    def edit_profile(session, user_id):
        user = session.query(User).filter(User.id == user_id).first()
        session.close()
        if user.phone_number[0] != "+":
            user.phone_number = user.phone_number.replace("8", "+7", 1)
        form = EditProfileForm(obj=user)
        BaseUserOptions.edit_user("profile_user", user_id, form, session, {})
        return form

    @staticmethod
    def see_profile(session, user_id):
        profile = session.query(User).filter(User.id == user_id).first()
        admin_user = session.query(User).filter(User.id == current_user.id).first()
        profile.phone_number = profile.phone_number.replace("8", "+7", 1)
        session.close()
        return {"profile": profile, "user": admin_user}

    @staticmethod
    def search_profile(form, session):
        if form.validate_on_submit() and request.method == "POST":
            user_search_data = form.search.data
            result = session.query(User).filter(or_(User.login.like(f"%{user_search_data}%"),
                                                    User.phone_number.like(f"%{user_search_data}%"),
                                                    User.first_name.like(f"%{user_search_data}%"),
                                                    User.second_name.like(f"%{user_search_data}%"),
                                                    User.surname.like(f"%{user_search_data}%"))).all()
            session.close()
        else:
            result = session.query(User).all()
        return result


class AdminUserOptions(BaseUserOptions):

    @staticmethod
    def edit_profile_user(session, user_id):
        user = session.query(User).filter(User.id == current_user.id).first()
        profile = session.query(User).filter(User.id == user_id).first()
        context_data = {"profile": profile}
        session.close()
        form = None
        if user.is_admin and profile is not None:
            if profile.phone_number[0] != "+":
                profile.phone_number = profile.phone_number.replace("8", "+7", 1)
            form = EditProfileForm(obj=profile)
            BaseUserOptions.edit_user("edit_profile_user", user_id, form, session, value_url={"user_id": user_id})
        return context_data, form

    @staticmethod
    def delete_user(user_id, session):
        user = session.query(User).filter(User.id == current_user.id).first()
        profile = session.query(User).filter(User.id == user_id).first()
        if user.is_admin and profile is not None:
            session.query(User).filter(User.id == profile.id).delete()
            session.commit()
            session.close()
            return True, user
        return False, user

    @staticmethod
    def add_user(session, form):
        user = session.query(User).filter(User.id == current_user.id).first()
        if user.is_admin:
            new_user = BaseUserOptions.create_user(form, session)
            if new_user is not None:
                return True
        return False

    @staticmethod
    def send_message(form, user_recipient):
        msg = None
        if form.validate_on_submit():
            message = form.message.data
            title = form.title.data
            print(user_recipient.email_name)
            msg = Message(body=message, subject=title, recipients=[user_recipient.email_name])
        return msg


