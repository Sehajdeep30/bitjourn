from flask import Flask, render_template, request
from datetime import datetime
from contenthandler import ContentHandler
import os

contentHandler = ContentHandler(w3token=os.getenv("W3STORAGE_TOKEN"))
app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/about")
def about_page():
    return render_template("about.html")


@app.route("/create")
def create_post():
    return render_template("create.html")


@app.route("/api/submit", methods=["POST"])
def api_submit():
    post_obj = {}
    post_obj["title"] = request.form["title"].strip()
    post_obj["author"] = request.form["author"].strip()
    post_obj["content"] = request.form["content"].strip()
    post_obj["timestamp"] = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    # sanitize tags
    tags = request.form["tags"].split(",")
    tags = [tag.strip() for tag in tags if tag.strip() != ""]
    post_obj["tags"] = tags

    post_obj["banner_url"] = request.form["banner"].strip()

    post_cid = contentHandler.create_post(post_obj)

    return f"your post is available at IPFS CID <code>{post_cid}</code>"


if __name__ == "__main__":
    app.run(debug=True)
