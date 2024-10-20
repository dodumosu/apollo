# -*- coding: utf-8 -*-
from functools import partial

from flask import Blueprint, g, url_for
from flask_babel import lazy_gettext as _
from flask_menu import register_menu
from flask_security import login_required

from apollo.formsframework.models import Form
from apollo.frontend import permissions, route
from apollo.result_analysis.results import voting_results
from apollo.result_analysis.turnout import turnout_convergence
from apollo.services import forms


def get_result_analysis_menu():
    """Menu generator for results summary."""
    event = g.event
    return [
        {
            "url": url_for("result_analysis.results_analysis", form_id=form.id),
            "text": form.name,
        }
        for form in forms.query.filter(
            Form.is_hidden == False,  # noqa
            Form.events.contains(event),
            Form.form_type == "CHECKLIST",
            Form.vote_shares != None,  # noqa
            Form.vote_shares != [],
        ).order_by("name")
    ]


def get_turnout_menu():
    """Menu generator for turnout."""
    event = g.event
    return [
        {
            "url": url_for("result_analysis.turnout", form_id=form.id),
            "text": form.name,
        }
        for form in forms.query.filter(
            Form.events.contains(event), Form.form_type == "CHECKLIST", Form.turnout_fields != []
        ).order_by("name")
    ]


bp = Blueprint(
    "result_analysis", __name__, template_folder="templates", static_folder="static", static_url_path="/core/static"
)


@route(bp, "/results_summary/<form_id>")
@register_menu(
    bp,
    "main.analyses.results_analysis",
    _("Results Data"),
    dynamic_list_constructor=partial(get_result_analysis_menu),
    visible_when=lambda: len(get_result_analysis_menu()) > 0 and permissions.view_result_analysis.can(),
)
@login_required
@permissions.view_result_analysis.require(403)
def results_analysis(form_id):
    """Results summary view."""
    return voting_results(form_id)


@route(bp, "/results_summary/<form_id>/<location_id>")
@login_required
@permissions.view_result_analysis.require(403)
def results_analysis_with_location(form_id, location_id):
    """Results summary with location view."""
    return voting_results(form_id, location_id)


@route(bp, "/turnout/<form_id>")
@register_menu(
    bp,
    "main.analyses.turnout",
    _("Partial Turnout Data"),
    dynamic_list_constructor=partial(get_turnout_menu),
    visible_when=lambda: len(get_turnout_menu()) > 0 and permissions.view_result_analysis.can(),
)
@login_required
@permissions.view_result_analysis.require(403)
def turnout(form_id):
    """Turnout view."""
    return turnout_convergence(form_id)


@route(bp, "/turnout/<form_id>/<location_id>")
@login_required
@permissions.view_result_analysis.require(403)
def turnout_with_location(form_id, location_id):
    """Turnout with location view."""
    return turnout_convergence(form_id, location_id)
