from flask import Blueprint
from flask import g
from flask import redirect
from flask import render_template
from flask import url_for
import flaskr.db
from time import time

bp = Blueprint("user", __name__)


@bp.route("/")
def index():
    if g.user is not None:
        database = flaskr.db.get_db()
        users = database.execute("SELECT * FROM user ORDER BY id DESC").fetchall()
        user = 0
        for i in users:
            if g.user["id"] == i["id"]:
                user = i
        if g.user["money"] is None:
            database.execute(
                "UPDATE user SET money = 1, cost_upgrade_click = 10, cost_upgrade_autoclicker = 10, coins_per_click = 1, coins_per_sec = 1, last_time = ? WHERE id = ?",
                (time(), str(g.user["id"]))).fetchall()
        else:
            auto_click = 0
            if time() - user["last_time"] < 0.1:
                auto_click = 0
            else:
                auto_click = user["coins_per_click"] + (time() - user["last_time"]) * user["coins_per_sec"]
            database.execute(
                "UPDATE user SET money = money + ?, last_time = ? WHERE id = ?",
                (int(auto_click), time(), str(g.user["id"]))).fetchall()
        database.commit()
        return render_template("index.html", user=user)
    return redirect(url_for("auth.login"))


@bp.route("/upgrade_autoclicker")
def upgrade_autoclicker():
    if g.user is not None:
        database = flaskr.db.get_db()
        users = database.execute("SELECT * FROM user ORDER BY id DESC").fetchall()
        user = 0
        for i in users:
            if g.user["id"] == i["id"]:
                user = i
        if user["money"] >= user["cost_upgrade_autoclicker"]:
            database.execute(
                "UPDATE user SET money = money - cost_upgrade_autoclicker, cost_upgrade_autoclicker = cost_upgrade_autoclicker * 2,  coins_per_sec = coins_per_sec * 2 WHERE id = ?",
                (str(g.user["id"]))).fetchall()
        database.commit()
        return render_template("upgrade_autoclicker.html", user=user)
    return redirect(url_for("auth.login"))


@bp.route("/upgrade_click")
def upgrade_click():
    if g.user is not None:
        database = flaskr.db.get_db()
        users = database.execute("SELECT * FROM user ORDER BY id DESC").fetchall()
        user = 0
        for i in users:
            if g.user["id"] == i["id"]:
                user = i
        if user["money"] >= user["cost_upgrade_click"]:
            database.execute(
                "UPDATE user SET money = money - cost_upgrade_click, cost_upgrade_click = cost_upgrade_click * 2, coins_per_click = ? WHERE id = ?",
                (int(user["coins_per_click"] * 2), str(g.user["id"]))).fetchall()
        database.commit()
        return render_template("upgrade_click.html", user=user)
    return redirect(url_for("auth.login"))
