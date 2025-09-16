import os
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'ここはランダムな秘密文字列'  # 適当にランダムに変更してください

# ------------------------
# サイト全体パスワード
# ------------------------
SITE_PASSWORD = 'pass123'  # サイト全体パスワード

# ------------------------
# 団体ログイン情報
# ------------------------
groups = {
    "3E": "pass123",
    "3F": "pass456"
}

# アップロード先
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ------------------------
# サイト全体ログイン画面
# ------------------------
@app.route("/", methods=["GET", "POST"])
def site_login():
    if session.get("site_logged_in"):
        return redirect(url_for("index"))  # ログイン済みならトップへ

    if request.method == "POST":
        password = request.form.get("password", "")
        if password == SITE_PASSWORD:
            session["site_logged_in"] = True
            return redirect(url_for("index"))
        else:
            return render_template("site_login.html", error="パスワードが違います")

    return render_template("site_login.html", error=None)

# ------------------------
# トップページ
# ------------------------
@app.route("/index")
def index():
    if not session.get("site_logged_in"):
        return redirect(url_for("site_login"))
    return render_template("index.html")

# ------------------------
# 団体ログイン
# ------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if not session.get("site_logged_in"):
        return redirect(url_for("site_login"))

    if request.method == "POST":
        group = request.form.get("group", "").strip()
        password = request.form.get("password", "").strip()
        if groups.get(group) == password:
            session["group"] = group
            return redirect(url_for("group_page", group_name=group))
        else:
            return render_template("login.html", error="団体名またはパスワードが違います")

    return render_template("login.html", error=None)

# ------------------------
# ログアウト
# ------------------------
@app.route("/logout")
def logout():
    session.clear()  # サイト全体ログインも団体ログインも消す
    return redirect(url_for("site_login"))

# ------------------------
# 団体ページ
# ------------------------
@app.route("/group/<group_name>", methods=["GET", "POST"])
def group_page(group_name):
    if not session.get("site_logged_in") or session.get("group") != group_name:
        return "アクセスできません"

    if request.method == "POST":
        file = request.files.get("file")
        if file:
            group_folder = os.path.join(UPLOAD_FOLDER, group_name)
            os.makedirs(group_folder, exist_ok=True)
            file.save(os.path.join(group_folder, file.filename))
            return f"{file.filename} をアップロードしました"

    return render_template("group.html", group_name=group_name)

# ------------------------
# Aboutページ
# ------------------------
@app.route("/about")
def about():
    if not session.get("site_logged_in"):
        return redirect(url_for("site_login"))
    return "<h2>このサイトについて</h2><p>文化祭の情報をまとめたサイトです。</p>"

# ------------------------
# 実行
# ------------------------
if __name__ == "__main__":
    app.run(debug=True)
