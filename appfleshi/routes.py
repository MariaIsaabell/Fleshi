from urllib import request

from dns.dnssec import validate
from flask import render_template, url_for, redirect
from flask_login import login_required, login_user, logout_user, current_user
from flask_wtf.file import file_required
from wtforms.validators import none_of
import os
from werkzeug.utils import secure_filename

from appfleshi.forms import LoginForm, RegisterForm, PhotoForm, ProfilePhotoForm
from appfleshi import app, database, bcrypt
from appfleshi.models import User, Photo

from appfleshi import app

@app.route('/', methods=['GET', 'POST'])
def homepage():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(email=login_form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, login_form.password.data):
            login_user(user)
            return redirect(url_for('feed'))

    return render_template('homepage.html', form=login_form)

@app.route('/createaccount', methods=['GET', 'POST'])
def createaccount():
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        password = bcrypt.generate_password_hash(register_form.password.data)
        user = User(username=register_form.username.data, password=password, email=register_form.email.data)
        database.session.add(user)
        database.session.commit()
        login_user(user, remember=True)
        return redirect(url_for('profile', user_id=user.id))
    return render_template('createaccount.html', form=register_form)

@app.route('/profile/<user_id>', methods=['GET', 'POST'])
@login_required
def profile(user_id, photo_form=None):
    if int(user_id) == int(current_user.id):
        photo_form = PhotoForm()
        if photo_form.validate_on_submit():
            file = photo_form.photo.data
            secure_name = secure_filename(file.filename)
            path = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], secure_name)
            file.save(path)
            photo = Photo(file_name=secure_name, user_id=current_user.id)
            database.session.add(photo)
            database.session.commit()
        return render_template('profile.html', user=current_user, form=photo_form)
    else:
        user = User.query.get(int(user_id))
        return render_template('profile.html', user=user, form=None)

@app.route('/delete/<int:photo_id>', methods=['POST'])
def delete_photos(photo_id):
    photo = Photo.query.get(photo_id)

    if not photo:
        excluir = ('Foto não encontrada!')
        return redirect(url_for('profile', user_id=current_user.id))

    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], photo.file_name)
    # Verifica se o arquivo existe no caminho especificado
    if os.path.exists(path):
        os.remove(path)
    else:
        print(f"Arquivo não encontrado: {path}")

    database.session.delete(photo)
    database.session.commit()

    return redirect(url_for('profile', user_id=current_user.id))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('homepage'))

@app.route("/feed")
@login_required
def feed():
    photos = Photo.query.order_by(Photo.upload_date.desc()).all()
    return render_template("feed.html", photos=photos)

@app.route("/photoperfil", methods=['GET', 'POST'])
@login_required
def photoperfil():
    form_profile = ProfilePhotoForm()

    if form_profile.validate_on_submit():
        file = form_profile.photo.data
        secure_name = secure_filename(file.filename)

        # CORREÇÃO AQUI: Salvar na pasta 'profile_photos' e não na 'posts_photos'
        upload_path = os.path.join(app.root_path, 'static', 'profile_photos', secure_name)
        file.save(upload_path)

        current_user.profile_photo = secure_name
        database.session.commit()

        return redirect(url_for("profile", user_id=current_user.id))

    return render_template("photoperfil.html", form_profile=form_profile)



