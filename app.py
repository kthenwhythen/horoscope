from flask import Flask, render_template, redirect, url_for, make_response, request
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


ZODIACS = {"Овен": "aries", "Телец": "taurus", "Близнецы": "gemini", "Рак": "cancer",
           "Лев": "leo", "Дева": "virgo", "Весы": "libra", "Скорпион": "scorpio",
           "Стрелец": "sagittarius", "Козерог": "capricorn", "Водолей": "aquarius", "Рыбы": "pisces"}
HEADER = {"Accept-Language": "ru-RU, ru;q=0.9,en-US;q=0.8,en;q=0,7",
          "User-Agent": "Mozilla/5.0 (Macitosh; Intel Mac OS X 11_2_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36",}
EVIL = ["З̘̮͓̂͌̐̂͛̑͑͊̒̚ͅа͖͈̯͍͉͈̥̗̬̭̟̏̓͆̽̏̓͒̿̒̈̑̊ͅв̫͍̮̝͛̊͐̅͐̀̓̄́͗ͅт̪͙̩͍̱̿͐̿̀̓̊́̂͂͒р̮͙̮̲̥͎̏̀̆̒̉̚̚а̘̫̤̯̥̦͕̪̤̪̤̭̾̿̒͂̈̾̀͌́̐̒ т̤͚͇̦͚̘̠̪̲̤̲̓͛͊͆͊́ы͖̝̳͎͕͙̖̗̥͒͒͑̏̽̅̂ у̮͇͍̦͔̦̣͊̏͒̀́͂̅̀̾м̞̗̙̟̩̟̈͒̅̀͊̈́̍р͙͕͙̜̦̮̞̏̌̅̂́͊̄̆̈́е̦̞̮̩͙͖͖̖̳̐͒̋̐̀͆̾̎͗̐̉̈́ш̮̲̘̝͚̬͖̞͉̈́̈́̓̿̎ь̘̪̮̤͌͂͂̄͛ͅ", "С̳̤͉͍̠̪̱̪̩͗̈̾̅̄̂̈̚м͚͎̳̞̭̭͔͈̞̫̱͔̝͍̩͇̊̍̾̈̊̅̅̽̋͗̽̇̌̑е͕͖͙͔͖͇̤̳̾̔͑̓͗̈͆̅͋р͔͚̳̗̰̫̟͖̝͈̲̎͒̍̎̅͛͌́̈́̈́͑̓т͈̥͇͎̣̫̯̳̤̞̠͊͊̄̌̓͊̅̽́͊͒̀ь̭̘͕̙̙͙͉̟̖͈̝́̇͂͋̿͋̅̾͊", "Д͍͈̗̦̣͙̰͉̰̠̱͈̈̽̍̀́̆̽̏̒̊̇̿̽̚о̮̫̣̙̪̫̝̱͖̜͈̯̤̩̮̥̩̫͑̈͆͐̑̃̎̽̋͒́͐̒͌͗̀͐̽̅̐͂̚б͎̱̘͖͇͚͇̲̟̭̬̭̫̗͓̙͇͒̀̎̐̅͂̌͗̓̏̿͛̒̇̿̏̌̉̄̊̚ͅр̥̣̦̙̤̝̯̮͍͍̜͓̦͈̱̗̫̊̎̃͌̃́̄̈̑̀̉̐͋̚ͅͅо̜͓̝̘͚͙͈̳͈̩̥̘̤͇͇̮̬͕̯̗̬́͐̔̅̾̀̇͆̓̉̿͋̉̏͛̍͋͐ п̱̮̦͔̥̳̥̦͙̝͓͇̮̲̝̠̞̥̰͉͙̣̠̮͑͛̊̌̌̾̅̓̇̽͋̅̇о͓̗̰̤̩͕͈̰̳̘͎͉̝̠̫̖͉̘͚̠̂̿̾̓͂̎̈́͐͋̈̋̈́̀͌̽̈̏̔̒̊̈́ͅж̘͈͇̠̟͇̫͈͈̩͎̩͇̜̖̦̥͔̱͔̱̝̠̅̒̔̊͊̉̃̾͑̊͐̑̇а̝̘̟̭̘̯̭̫̟̞͚͚̜͉̮̮̬̟̞͙͍͕̗͋̇͋̍̏̄̄́̊̍̏̒̍̀͐̐̊̂̔̐̈́͊̎̚л̘̖̳͍̯͍̗͈͙͔̩̫̗̟͖̘͛̈̈́͆̄̔̏̆̓͑̀̒̌̇͋̒ͅͅо͖̝͚̜͍̖̱͍̲̭̦̖̤̦̩̩̘́͌̏̒́̑͋͗͒̾͛̎̇̾̅̚ͅв̫̝̰̜̟͇̝͎̰͕̘̳̘̝̞̰̀̆̀̋͐̐̊̈́̑̓͛̂̽̂͌̀̂ͅа̦̭͕̘̱̩̯͓͔̘̜̞̠͎̗͇̂̃̏͆́̀̿̊͒̉͛̓̀͌ͅт̤͉͎͙͚̖̥͎̫͖̣͔̜͉̮͓̦̱̜͋̿͛̀̐͋̋̐̈́͛͊̈́̈͛̔ь̦͖͖̳̳͈̙͚͎̯͓̝̤̞̯̒̇̈́̾̃̅̅͂̅̄̽̐́͒̐ в͎͔̭̙͙͈͎̲͈̮̪̫̤̭͉͚̞͔͇͔͙̲̖̑̆̐̽̈̽͋̇͐̀͑̊̆̊͗̏̅͌͒̃͊ и̩͔̘̦͚͕͈͓̤͚̫̙̦̳͉̽̾̈́͐͑̽͋̓̓͌̅͋̽̒̔͐̇͛̾̉͑̏̋̊с͓̟̯̪̳͖͓̣͇̜͍̙̗͉̏̋͌͊̑̆̉̍̈́̀̐̋̄̾̐̆͛̍̚ͅͅѐ̜̞̤̠̫̟̱̗̘̤̞̳͙̣̰̲͖̮͙̯̝̠̓͌̋͋̉̃͛̄͒͆̈́̌͂͛̅͛̓̿̃̋̉к̙̥̫̖͇͙̯̦̤͓̠͎̮͚̤̦̝̖̂̎̌̍͐͋̇̽͊͐̃́̽͒̔а͓̗̫̠̖̲͓͇̜̙̲͋͂́͛̃̓͊̄̅̊̑̓͆̊̒̆̏̓̓ͅй̮̥̱͙͇͉͓͇̖̭͍͍͙̩͙̽͋̈́̅̍͋̂̏̏̽̋̚ͅ"]


class CookieForm(FlaskForm):
    name = StringField("Имя", validators=[DataRequired()])
    zodiac = SelectField("Знак зодиака", choices=ZODIACS, validators=[DataRequired()])
    submit = SubmitField("Submit")


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
    if zodiac == "libra" and random.randint(1, 100) <= 5:
        prediction = random.choice(EVIL)
    else:
        response = requests.get(url=f"https://horo.mail.ru/prediction/{zodiac}/{day}/", headers=HEADER)
        soup = BeautifulSoup(response.text, "html.parser")
        prediction = soup.find("div", class_="article_prediction").find_all("p")
        prediction = prediction[0].contents[0] + " " + prediction[1].contents[0]
    return prediction


@app.route('/', methods=["GET", "POST"])
def index():
    if not request.cookies.get("zodiac") or not request.cookies.get("name"):
        return redirect(url_for("cookies"))
    
    name = request.cookies.get("name")
    zodiac = request.cookies.get("zodiac")
    predictions = {}
    # prediction_tomorrow = get_prediction(zodiac, "tomorrow")
    # prediction_yesterday = get_prediction(zodiac, "yesterday")
    predictions["today"] = get_prediction(zodiac, "today")
    return render_template("index.jade", path="img/logo-icon.svg", name=name, predictions=predictions)
    # today = str(datetime.datetime.today().strftime("%b-%d"))
    # if not request.cookies.get("time") == today:
    #     zodiac = request.cookies.get('zodiac')
    #     response = requests.get(url=f"https://horo.mail.ru/prediction/{zodiac}/today/", headers=HEADER)
    #     soup = BeautifulSoup(response.text, "html.parser")
    #     prediction = soup.find("div", class_="article_prediction").find_all("p")
    #     prediction = prediction[0].contents[0] + " " + prediction[1].contents[0]
    #     cookie = make_response("Set time")
    #     cookie.set_cookie("time", today, max_age=60*60*24*365)
    #     cookie.set_cookie(f'prediction {today}', prediction, max_age=60*60*24*7)

    #     cookie.headers["location"] = url_for("index")
    #     return make_response(cookie, 302)
    # prediction = request.cookies.get("prediction Mar-16")
    # return render_template('index.jade', path="img/logo-icon.svg", 
    #                         prediction=prediction,
    #                         name=request.cookies.get("name"))


@app.route("/cookies", methods=["GET", "POST"])
def cookies():
    form = CookieForm()
    if form.validate_on_submit():
        cookie = make_response("Setting a cookie")
        cookie.set_cookie("name", form.name.data, max_age=60*60*24*365)
        cookie.set_cookie("zodiac", ZODIACS[form.zodiac.data], max_age=60*60*24*365)
        cookie.headers['location'] = url_for('index')
        return make_response(cookie, 302)
    return render_template("cookie.jade", form=form)


if __name__ == '__main__':
    app.run(debug=True)
