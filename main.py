from flask import Flask, render_template, url_for, request, redirect
from flask_login import logout_user, login_user, login_required, current_user
from flask_login import LoginManager
from data import db_session
from data.users import User
from data.settings import Settings
from data.game_class import Game
from forms.login_form import LoginForm
from forms.register_form import RegisterForm
from forms.settings_form import SettingsForm
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

game = Game()
login_manager = LoginManager()
login_manager.init_app(app)


def main():
    db_session.global_init("db/dataBase.db")
    db_sess = db_session.create_session()
    # port = int(os.environ.get("PORT", 5000))
    # app.run(host='0.0.0.0', port=port)
    app.run(port=8080, host='127.0.0.1')


def get_background():
    img = url_for('static', filename='img/default.jpg')
    if current_user.is_authenticated:
        db_sess = db_session.create_session()
        setting = db_sess.query(Settings).filter(Settings.user == current_user).first()
        if setting.theme == 'default':
            img = url_for('static', filename='img/default.jpg')
        if setting.theme == 'magic girl':
            img = url_for('static', filename='img/girl.jpg')
        if setting.theme == 'Odyssey':
            img = url_for('static', filename='img/odyssey.jpg')
        if setting.theme == 'lonely mountain':
            img = url_for('static', filename='img/mountain.jpg')
        if setting.theme == 'people routine':
            img = url_for('static', filename='img/people_routine.jpg')
        if setting.theme == 'winter dreams':
            img = url_for('static', filename='img/dreams.jpg')
        if setting.theme == 'house in the forest':
            img = url_for('static', filename='img/house_in_the_forest.jpg')
    return img


def get_numbers_of_cards():
    if current_user.is_authenticated:
        db_sess = db_session.create_session()
        setting = db_sess.query(Settings).filter(Settings.user == current_user).first()
        return setting.cards_in_deck, setting.cards_in_hand
    return 62, 6


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/', methods=['GET', 'POST'])
def main_page():
    if request.method == 'GET':
        param = dict()
        param['img'] = get_background()
        param['title'] = "Main page"
        return render_template('main.html', **param)
    elif request.method == 'POST':
        global game
        if request.form.get('names'):
            quick_game = False
            if request.form.get('quick_game'):
                quick_game = request.form['quick_game']
            names = [x.strip() for x in request.form['names'].split('\n')]
            code = game.add(names, get_numbers_of_cards(), quick_game=quick_game)
            if not code:
                return redirect(f'/too_many_games')
        if request.form.get('code'):
            code = request.form['code']
        if not game.is_valid_code(code):
            return redirect(f'/wrong/{code}')
        return redirect(f'/gamecode/{code}')


@app.route('/gamecode/field/<code>')
def main_pole(code):
    if not game.is_valid_code(code):
        return redirect(f'/wrong/{code}')
    if game.is_win(code):
        return redirect(f'/win/{code}')
    param = {}
    progress = game.players_progress(code)
    param['title'] = f"Playing field '{code}'"
    param['progress'] = progress
    param['cards'] = [url_for('static', filename=x) for x in game.choosen_images(code)]
    param['img'] = get_background()
    param['assotiation'] = game.get_assotiation(code)
    return render_template('field.html', **param)


@app.route('/gamecode/player_cards/<string:code>/<name>', methods=['POST', 'GET'])
def player(code, name):
    global game
    if request.method == 'GET':
        if not game.is_valid_code(code):
            return redirect(f'/wrong/{code}')
        if game.is_win(code):
            return redirect(f'/win/{code}')
        param = dict()
        param['direct'] = game.who_is_directing(code)
        param['img'] = get_background()
        param['points'] = game.get_points(code)[name]
        param['place'] = game.player_place(code, name)
        param['title'] = f'Cards for {name}'
        param['choosing'] = game.is_choosing(code)
        param['voting'] = game.is_voting(code)
        param['self_choose'] = game.is_choose(code, name)
        param['self_vote'] = game.is_vote(code, name)
        param['self_directing'] = (game.who_is_directing(code) == name)
        param['max_number_of_cards'] = game.max_number_of_cards(code, name)
        param['cards'] = [url_for('static', filename=x) for x in game.cards(code, name)]
        return render_template('player.html', **param)
    if request.method == 'POST':
        if not game.is_valid_code(code):
            return redirect(f'/wrong/{code}')
        if request.form.get('choice'):
            num = int(request.form['choice'])
            game.somebody_choose(code, name, num)
        if request.form.get('vote'):
            num = int(request.form['vote'])
            game.somebody_vote(code, name, num)
        if request.form.get('assotiation'):
            ass = request.form['assotiation']
            game.set_assotiation(code, ass)
        return redirect(f'/gamecode/player_cards/{code}/{name}')


@app.route('/gamecode/<code>')
def gamecode(code):
    global game
    if not game.is_valid_code(code):
        return redirect(f'/wrong/{code}')
    if game.is_win(code):
        return redirect(f'/win/{code}')
    param = dict()
    param['title'] = f'Game {code}'
    param['code'] = code
    param['img'] = get_background()
    param['players'] = game.get_names(code)
    return render_template('gamecode_page.html', **param)


@app.route('/wrong/<code>')
def wrongcode(code):
    param = dict()
    param['title'] = f'Wrong code - {code}'
    param['img'] = get_background()
    return render_template('wrongcode.html', **param)


@app.route('/rules')
def rules():
    param = dict()
    param['title'] = 'Main page'
    param['img'] = get_background()
    return render_template('rules.html', **param)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Register',
                                   form=form,
                                   message="Passwords don't match", img=get_background())
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Register',
                                   form=form,
                                   message="We have such user", img=get_background())
        user = User(
            name=form.name.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        setting = Settings(theme='dark', user=user)
        db_sess.add(user)
        db_sess.add(setting)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Register', form=form, img=get_background())


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Wrong password or name",
                               form=form, img=get_background())
    return render_template('login.html', title='Authorisation', form=form, img=get_background())


@app.route('/settings', methods=['GET', 'POST'])
def settings():
    form = SettingsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        setting = db_sess.query(Settings).filter(Settings.user == current_user).first()
        setting.theme = form.theme.data
        setting.cards_in_hand = form.number_of_cards_in_hand.data
        setting.cards_in_deck = form.number_of_cards_in_deck.data
        db_sess.commit()
        return redirect("/")
    return render_template('settings.html', title='Settings', form=form, img=get_background())


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/win/<code>')
def win(code):
    if not game.is_valid_code(code):
        return redirect(f'/wrong/{code}')
    param = dict()
    param['img'] = get_background()
    param['title'] = 'Game over'
    param['winners'] = game.is_win(code)
    return render_template('win.html', **param)


@app.route('/too_many_games')
def too_many():
    param = dict()
    param['img'] = get_background()
    param['title'] = 'Too many games'
    return render_template('too_many_games.html')


@app.route('/brief_guide')
def about():
    param = dict()
    param['img'] = get_background()
    param['title'] = 'Brief guide'
    return render_template('about.html', **param)


@app.errorhandler(500)
def internal_error():
    param = dict()
    param['img'] = get_background()
    param['title'] = 'Mistake:('
    return render_template('500.html'), 500


@app.errorhandler(404)
def internal_error():
    param = dict()
    param['img'] = get_background()
    param['title'] = 'Come back'
    return render_template('404.html'), 404


if __name__ == '__main__':
    main()
