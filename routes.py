from crypt import methods
from flask import Flask
import views

def setup_routes(app: Flask):
    app.add_url_rule("/", view_func=views.index)
    app.add_url_rule("/about", view_func=views.about)
    app.add_url_rule("/about/write", view_func=views.write_post, methods=["GET", "POST"])
    app.add_url_rule("/about/edit", view_func=views.write_post, methods=["GET", "POST"])
    app.add_url_rule("/rules", view_func=views.rules)
    app.add_url_rule("/rules/write", view_func=views.write_rules, methods=["GET", "POST"])
    app.add_url_rule("/rules/edit", view_func=views.write_rules, methods=["GET", "POST"])
    app.add_url_rule("/notices", view_func=views.notices)
    app.add_url_rule("/notices/<int:no>", view_func=views.notices)
    app.add_url_rule("/notices/<int:no>", view_func=views.delete_post, methods=["DELETE"])
    app.add_url_rule("/notices/write", view_func=views.write_post, methods=["GET", "POST"])
    app.add_url_rule("/notices/<int:no>/edit", view_func=views.write_post, methods=["GET", "POST"])
    app.add_url_rule("/classes", view_func=views.classes)
    app.add_url_rule("/classes/<name>", view_func=views.classes)
    app.add_url_rule("/classes/<name>/<int:no>", view_func=views.classes)
    app.add_url_rule("/classes/<name>/<int:no>", view_func=views.delete_class_activity, methods=["DELETE"])
    app.add_url_rule("/classes/<name>/write", view_func=views.write_class_activity, methods=["GET", "POST"])
    app.add_url_rule("/classes/<name>/<int:no>/edit", view_func=views.write_class_activity, methods=["GET", "POST"])
    app.add_url_rule("/magazines", view_func=views.magazines)
    app.add_url_rule("/magazines/<int:no>", view_func=views.magazines)
    app.add_url_rule("/magazines/<int:no>", view_func=views.delete_magazine, methods=["DELETE"])
    app.add_url_rule("/magazines/write", view_func=views.write_magazine, methods=["GET", "POST"])
    app.add_url_rule("/magazines/<int:no>/edit", view_func=views.write_magazine, methods=["GET", "POST"])
    app.add_url_rule("/uploaded/<filename>", view_func=views.uploaded)
    app.add_url_rule("/register", view_func=views.register, methods=["POST"])
    app.add_url_rule("/login", view_func=views.login, methods=["POST"])
    app.add_url_rule("/logout", view_func=views.logout)
    app.add_url_rule("/admin", view_func=views.admin)
    app.add_url_rule("/users/<int:id>/modify", view_func=views.modify_user)
    app.add_url_rule("/info", view_func=views.edit_club_info, methods=["POST"])
    app.add_url_rule("/class-info", view_func=views.edit_class_info, methods=["POST"])