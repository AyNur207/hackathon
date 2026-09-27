import datetime
from flask import Flask, render_template, url_for, jsonify, make_response, request, redirect
from flask_restful import Api
from data import db_session
from data.users_resources import UsersResource, UsersListResources
from forms.login_form import LoginForm
from forms.register_form import RegForm
from data2 import TESTS

from os.path import join, normpath
from werkzeug.utils import secure_filename
from flask_login import LoginManager, login_user, logout_user, login_required
from data.user import Users
import config
import pymorphy3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDERS
api = Api(app)
login_manager = LoginManager()
login_manager.init_app(app)
morph = pymorphy3.MorphAnalyzer()


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(Users).get(user_id)


n = 0

@app.route('/')
def index():
  return render_template('index.html', tests=TESTS)



@app.route("/test/<topic>")
def test(topic):
    """Страница прохождения теста."""
    if topic not in TESTS:
        return redirect(url_for("index"))
    return render_template("test.html", topic=topic, test=TESTS[topic])


@app.route("/result", methods=["POST"])
def result():
    """Обработка ответов и вывод результата."""
    topic = request.form.get("topic")
    if topic not in TESTS:
        return redirect(url_for("index"))

    test = TESTS[topic]
    counts = {"А": 0, "Б": 0, "В": 0, "Г": 0}

    # Считаем ответы (в форме поля answers_0, answers_1, ...)
    for key, value in request.form.items():
        if key.startswith("answers_") and value in counts:
            counts[value] += 1

    # Находим букву-победителя
    winner = max(counts, key=counts.get)
    top_result = test["results"][winner]

    # Считаем процент совпадения
    total = sum(counts.values()) or 1
    percent = round(counts[winner] / total * 100)

    return render_template(
        "result.html",
        topic=topic,  # Передаем тему, чтобы кнопка "Пройти заново" работала
        test=test,
        result=top_result,
        winner=winner,
        percent=percent,
    )


@app.route('/profile/<int:id>')  # обработчик профиля пользователя
def profile(id):
    session = db_session.create_session()
    user = session.query(Users).filter(Users.id == id).first()
    photo = session.query(Users).all()
    return render_template('profile.html', title='Профиль', user=user, photos=photo,
                           css1=url_for('static', filename='css/style_profile.css'))

@app.route('/register', methods=['GET', 'POST'])
def register():  # регистрация
    form = RegForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if db_sess.query(Users).filter(Users.email == form.email.data).first():  # проверка логина и пароля пользователя
            return render_template('registration.html', title='Регистрация', form=form, message='такая почта уже есть')
        if db_sess.query(Users).filter(Users.login == form.login.data).first():
            return render_template('registration.html', title='Регистрация', form=form, message='такой логин уже есть')
        if form.password.data != form.password_again.data:
            return render_template('registration.html', title='Регистрация', form=form, message='пароли не совпадают')
        if request.files['file']:
            file = request.files['file']  # добавление изображения профиля в бд
            filename = secure_filename(file.filename)
            path = normpath(join(app.config['UPLOAD_FOLDER']['PROFILE_IMAGES_FOLDER'], filename))
            file.save(path)
        else:
            path = join(app.config['UPLOAD_FOLDER']['PROFILE_IMAGES_FOLDER'], 'default_image.png')
        user = Users(  # добавление пользователя
            login=form.login.data,
            email=form.email.data,
            photo=path,
            phone_number=form.phone_number.data,
            created_date=datetime.datetime.now()
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        login_user(user)
        return redirect('/')
    return render_template('registration.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():  # авторизация пользователя
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(Users).filter(Users.login == form.login.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', form=form, title='Авторизация')
@app.route('/maps')

def maps():
    return render_template('maps.html')


@app.errorhandler(400)  # обработчик ошибки 400
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)
@app.errorhandler(401)
def unauthorized(_):  # обработка ошибки, если пользователь не авторизован
    return redirect('/login')


@app.route('/logout')
@login_required
def logout():  # выход из аккаунта
    logout_user()
    return redirect("/")

def main():
    db_session.global_init("db/uunit_db.db")
    api.add_resource(UsersResource, '/api/users/<int:users_id>')
    api.add_resource(UsersListResources, '/api/users')
    app.run(port=8080, host='127.0.0.1')


if __name__ == '__main__':
    main()