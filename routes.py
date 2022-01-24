from crypt import methods
from flask import Flask
import views

def setup_routes(app: Flask):
    app.add_url_rule("/", view_func=views.index)
    app.add_url_rule("/about", view_func=views.about)
    app.add_url_rule("/about/write", view_func=views.write_post, methods=["GET", "POST"])
    app.add_url_rule("/about/edit", view_func=views.write_post, methods=["GET", "POST"])
    app.add_url_rule("/notices", view_func=views.notices)
    app.add_url_rule("/notices/<int:no>", view_func=views.notices)
    app.add_url_rule("/notices/<int:no>", view_func=views.delete_post, methods=["DELETE"])
    app.add_url_rule("/notices/write", view_func=views.write_post, methods=["GET", "POST"])
    app.add_url_rule("/notices/<int:no>/edit", view_func=views.write_post, methods=["GET", "POST"])
    app.add_url_rule("/uploads/<name>", view_func=views.download)
    app.add_url_rule("/classes", view_func=views.classes)
    app.add_url_rule("/classes/<name>", view_func=views.classes)
    app.add_url_rule("/classes/<name>/<int:no>", view_func=views.classes)
    app.add_url_rule("/classes/<name>/<int:no>", view_func=views.delete_class_activity, methods=["DELETE"])
    app.add_url_rule("/classes/<name>/write", view_func=views.write_class_activity, methods=["GET", "POST"])
    app.add_url_rule("/classes/<name>/<int:no>/edit", view_func=views.write_class_activity, methods=["GET", "POST"])