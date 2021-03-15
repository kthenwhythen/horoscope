from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_assets import Environment, Bundle


# Flask app init
app = Flask(__name__)

# Flask app config
app.config['SECRET_KEY'] = 'TEMP_SECRET_KEY'

# Flask extensions
# Ext for Jade support
app.jinja_options['extensions'].append('pyjade.ext.jinja.PyJadeExtension')

# Bootstrap init
Bootstrap(app)

# Sass support init
assets = Environment(app)
sass = Bundle('css/sass/style.sass',
              filters='libsass',
              output='css/style.css',
              depends='**/*.sass')
assets.register('sass_all', sass)


@app.route('/')
def index():
    return render_template('index.jade', path="img/logo-icon.svg")


if __name__ == '__main__':
    app.run(debug=True)
