from flask import Flask, render_template, redirect, flash
import db_session
from thing import ThingsForm
from things import Things
from users import User
from user import RegisterForm, LoginForm
import db_methods
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)

app.secret_key = 'yandexlyceum_secret_key'


@app.route("/")
def index():
    return render_template("homepage.html")


@app.route("/clothes")
def clothes():
    clothes = db_methods.Thing.get_all()
    return render_template("clothes.html",
                           clothes_list=clothes)


@app.route("/thing/<int:id>")
def thing(id):
    clothes = db_methods.Thing.get_by_id(id)
    return render_template("details.html",
                           thing=clothes)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/clothes")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/clothes")


@app.route('/new_thing',  methods=['GET', 'POST'])
@login_required
def add_news():
    if current_user.email != 'fedorlegend@mail.ru':
        return redirect('/')
    form = ThingsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        things = Things()
        things.type = form.type.data
        things.name = form.name.data
        things.price = form.price.data
        things.imgurl = form.imgurl.data
        things.color = form.color.data
        things.size = form.size.data
        things.availbility = form.availbility.data
        db_sess.merge(things)
        db_sess.commit()
        return redirect('/')
    return render_template('new_thing.html', title='Добавление вещи',
                           form=form)


@app.route('/add-to-cart/<int:thing_id>')
def add_to_cart(thing_id):
    if current_user.is_authenticated:
        thing = db_methods.Thing.get_by_id(thing_id)
        if thing:
            new_item = db_methods.Cart(thing_id=thing_id, user_id=current_user.id, price=thing.price)
            db_methods.Cart.add_to_cart(new_item)
            flash('Товар успешно добавлен в корзину', 'success')
            return redirect('/clothes')
        else:
            flash('Товар не найден', 'error')
            return redirect('/clothes')
    else:
        flash('Для добавления товаров в корзину нужно войти в систему', 'error')
        return redirect('/login')


if __name__ == "__main__":
    db_session.global_init("templates/clothes.db")
    app.run(debug=True)
