from flask import Flask, render_template

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/about')
def about():
    name = 'about'
    return render_template(f"{name}.html", active=f"{name}")


@app.route('/atletas')
def atletas():
    name = 'atletas'
    return render_template(f"{name}.html", active=f"{name}")


@app.route('/abierto')
def abierto():
    name = 'abierto'
    return render_template(f"{name}.html", active=f"{name}")


@app.route('/productos')
def productos():
    name = 'productos'
    return render_template(f"{name}.html", active=f"{name}")
