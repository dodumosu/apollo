# -*- coding: utf-8 -*-
from flask import (
    Blueprint, abort, current_app, json, jsonify, redirect, render_template,
    request, session, url_for)
from flask_babelex import lazy_gettext as _
from flask_security import current_user, login_required
from flask_security.utils import hash_password

from apollo.core import db, red
from apollo.frontend import route
from apollo.users import forms, models

bp = Blueprint('users', __name__)


@route(bp, '/user/profile', methods=['GET', 'POST'])
@login_required
def user_profile():
    if current_user.has_role('field-coordinator'):
        abort(403)

    breadcrumbs = [_('Edit Profile')]
    user = current_user._get_current_object()
    form = forms.UserDetailsForm(instance=user)

    if form.validate_on_submit():
        data = form.data
        if data.get('password'):
            user.password = hash_password(data.get('password'))

        user.username = data.get('username')
        user.email = data.get('email')
        user.locale = data.get('locale') or None

        user.save()
        return redirect(url_for('dashboard.index'))

    context = {'form': form, 'breadcrumbs': breadcrumbs}

    return render_template('frontend/userprofile.html', **context)


@route(bp, '/user/tasks')
@login_required
def task_list():
    session_id = session.get('_id')

    # extract the data from Redis
    stringified_data = red.lrange(session_id, 0, -1)
    raw_data = [json.loads(d) for d in stringified_data]

    tasks = {
        'results': raw_data
    }

    return jsonify(tasks)


@route(bp, "/user/files")
@login_required
def user_file_list():
    template = "frontend/user_file_list.html"
    context = {
        "breadcrumbs": [_("My Files")],
        "page_title": _("My Files"),
        "form": forms.generate_user_file_delete_form_class(current_user)(),
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


@route(bp, "/user/files/delete", methods=["POST"])
@login_required
def user_file_delete():
    form = forms.generate_user_file_delete_form_class(current_user)()
    if form.validate_on_submit():
        user_files = form.data["user_files"]
        for user_file in user_files:
            db.session.delete(user_file)
        db.session.commit()

    return redirect(url_for("users.user_file_list"))
