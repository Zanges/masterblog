from flask import Flask, render_template, request, redirect, url_for

from dataprovider.jsonprovider import JsonProvider


provider = JsonProvider("./data.json")
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html", posts=provider.get_data())


@app.route("/add", methods=["GET", "POST"])
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
        return redirect(url_for("index"))
    return render_template("add.html")


@app.route("/delete/<int:post_id>")
def delete(post_id: int):
    provider.delete_data(post_id)
    return redirect(url_for("index"))


@app.route("/update/<int:post_id>", methods=["GET", "POST"])
def update(post_id: int):
    post = provider.get_data_by_id(post_id)
    if post is None:
        # Post not found
        return "Post not found", 404
    
    if request.method == "POST":
        title = request.form.get("title")
        author = request.form.get("author")
        content = request.form.get("content")
        data = {
            "id": post_id,
            "title": title,
            "author": author,
            "content": content
        }
        provider.update_data(post_id, data)
        return redirect(url_for("index"))
    return render_template("update.html", post=post)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)