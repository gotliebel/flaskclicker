from flask import Flask, render_template, url_for, request

app = Flask(__name__)

coin = 0


@app.route("/", methods=['GET', 'POST'])
def index():
    global coin
    if request.method == 'POST':
        if request.form.get('Click') == 'Click':
            coin += 1
            return render_template("index.html", var=coin)
    elif request.method == 'GET':
        return render_template("index.html", var=coin)


@app.route('/help')
def help():
    return 'Help'


@app.route('/about')
def about():
    return 'soon...'


if __name__ == '__main__':
    app.run()
