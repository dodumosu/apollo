# -*- coding: utf-8 -*-
from flask import (
    Blueprint,
    current_app,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_babelex import lazy_gettext as _
from flask_security import current_user, login_required

from apollo.core import db
from apollo.frontend import route
from . import forms, models

bp = Blueprint(
    "users", __name__, template_folder="templates", static_folder="static"
)


@route(bp, "/files")
@login_required
def user_file_list():
    template = "frontend/user_file_list.html"
    context = {
        "page_title": _("My Files"),
    }
    args = request.args.to_dict(flat=False)
    page = int(args.pop("page", [1])[0])

    files = models.UserGeneratedFile.query.filter_by(
        user=current_user
    ).order_by(models.UserGeneratedFile.created.desc())
    context["args"] = args
    context["pager"] = files.paginate(
        page=page, per_page=current_app.config.get("PAGE_SIZE")
    )

    return render_template(template, **context)


@route(bp, "/files/delete", methods=["POST"])
@login_required
def user_file_delete():
    form = forms.generate_user_delete_form_class(current_user)()
    if form.validate_on_submit():
        user_files = form.data["user_files"]
        for user_file in user_files:
            db.session.delete(user_file)
        db.session.commit()

    return redirect(url_for("users.user_file_list"))
