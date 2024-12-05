from flask import Flask, render_template, request

from dataprovider.jsonprovider import JsonProvider


provider = JsonProvider("./data.json")
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', posts=provider.get_data())


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)