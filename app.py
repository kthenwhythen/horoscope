from flask import Flask, render_template, redirect, url_for, make_response, request, jsonify
from flask_caching import Cache
from flask_bootstrap import Bootstrap
from flask_assets import Environment, Bundle
from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField
from wtforms.validators import DataRequired
import requests
from bs4 import BeautifulSoup
import datetime
import random
import evil


ZODIACS = {"Овен": "aries", "Телец": "taurus", "Близнецы": "gemini", "Рак": "cancer",
           "Лев": "leo", "Дева": "virgo", "Весы": "libra", "Скорпион": "scorpio",
           "Стрелец": "sagittarius", "Козерог": "capricorn", "Водолей": "aquarius", "Рыбы": "pisces"}
ZODIACS_REVERSE = {"aries": "Овен", "taurus": "Телец", "gemini": "Близнецы", "cancer": "Рак",
           "leo": "Лев", "virgo": "Дева", "libra": "Весы", "scorpio": "Скорпион",
           "sagittarius": "Стрелец", "capricorn": "Козерог", "aquarius": "Водолей", "pisces": "Рыбы"}
HEADER = {"Accept-Language": "ru-RU, ru;q=0.9,en-US;q=0.8,en;q=0,7",
          "User-Agent": "Mozilla/5.0 (Macitosh; Intel Mac OS X 11_2_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36",}


class CookieForm(FlaskForm):
    name = StringField("Имя", validators=[DataRequired()])
    zodiac = SelectField("Знак зодиака", choices=ZODIACS, validators=[DataRequired()])
    submit = SubmitField("Войти")


# Flask app init
app = Flask(__name__)

# Flask app config
app.config['SECRET_KEY'] = 'TEMP_SECRET_KEY'
app.config["CACHE_TYPE"] = "SimpleCache"

# Flask extensions
# Ext for Jade support
app.jinja_options['extensions'].append('pyjade.ext.jinja.PyJadeExtension')

# Bootstrap init
Bootstrap(app)

# Cache init
cache = Cache(app)

# Sass support init
assets = Environment(app)
sass = Bundle('css/sass/style.sass',
              filters='libsass',
              output='css/style.css',
              depends='**/*.sass')
assets.register('sass_all', sass)


@cache.memoize(60*60)
def get_prediction(zodiac, day):
    if zodiac == "libra" and random.randint(1, 100) <= 20 and day != "yesterday":
        prediction = random.choice(evil.evil)
    else:
        response = requests.get(url=f"https://horo.mail.ru/prediction/{zodiac}/{day}/", headers=HEADER)
        soup = BeautifulSoup(response.text, "html.parser")
        prediction = soup.find("div", class_="article_prediction").find_all("p")
        prediction = prediction[0].contents[0] + " " + prediction[1].contents[0]
    return prediction


@app.route('/')
def index():
    if not request.cookies.get("zodiac") or not request.cookies.get("name"):
        return redirect(url_for("cookies"))
    zodiac = request.cookies.get("zodiac")
    name = request.cookies.get("name")
    zodiac_ru = ZODIACS_REVERSE[zodiac]
    today = datetime.datetime.today()
    yesterday = today - datetime.timedelta(days=1)
    tomorrow = today + datetime.timedelta(days=1)
    dates = {"today": today.strftime("%d / %m / %Y"), "yesterday": yesterday.strftime("%d / %m / %Y"), "tomorrow": tomorrow.strftime("%d / %m / %Y")}
    return render_template("index.jade", path=f"img/logos/{zodiac}.svg", zodiac=zodiac_ru, dates=dates, name=name)


@app.route("/cookies", methods=["GET", "POST"])
def cookies():
    form = CookieForm()
    if form.validate_on_submit():
        cookie = make_response("Setting a cookie")
        cookie.set_cookie("name", form.name.data, max_age=60*60*24*365)
        cookie.set_cookie("zodiac", ZODIACS[form.zodiac.data], max_age=60*60*24*365)
        cookie.headers['location'] = url_for('index')
        return make_response(cookie, 302)
    if request.cookies.get("zodiac"):
        form.zodiac.data = ZODIACS_REVERSE[request.cookies.get("zodiac")]
    if request.cookies.get("name"):
        form.name.data = request.cookies.get("name")
    return render_template("cookie.jade", form=form)


@app.route("/prediction/<string:day>")
def prediction(day):
    zodiac = request.cookies.get("zodiac")
    prediction = get_prediction(zodiac, day)
    return prediction


if __name__ == '__main__':
    app.run()
