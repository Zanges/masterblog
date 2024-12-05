from flask import Flask, render_template, request, redirect, url_for

from dataprovider.jsonprovider import JsonProvider


provider = JsonProvider("./data.json")
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', posts=provider.get_data())


@app.route('/add', methods=["GET", "POST"])
def add():
    if request.method == "POST":
        title = request.form.get("title")
        author = request.form.get("author")
        content = request.form.get("content")
        data = {
            "id": provider.get_first_free_id(),
            "title": title,
            "author": author,
            "content": content
        }
        provider.add_data(data)
        return redirect(url_for('index'))
    return render_template('add.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)