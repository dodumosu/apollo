# -*- coding: utf-8 -*-
import time

import flask_wtf as wtf
import wtforms
from flask import g

from apollo import models, services


class MessagesFilterForm(wtf.FlaskForm):
    mobile = wtforms.StringField()
    text = wtforms.StringField()
    date = wtforms.DateField(format="%d-%m-%Y")


class BaseHttpForm(wtforms.Form):
    """Helper form for validating incoming messages."""

    def get_message(self):
        return NotImplementedError()


class KannelForm(wtforms.Form):
    """Django-based form for validating incoming messages from a Kannel-based SMS gateway.

    :param sender: The phone number of the sender.
    :param text: The contents of the text message.
    :param charset: (Optional) character set for handling incoming message.
    :param coding: (Optional) not being used at the moment.
    """

    sender = wtforms.StringField(validators=[wtforms.validators.data_required()])
    text = wtforms.StringField(validators=[wtforms.validators.data_required()])
    charset = wtforms.StringField()
    coding = wtforms.StringField()
    timestamp = wtforms.IntegerField()

    def clean_text(self):
        charset = self.charset.data
        text = self.text.data
        if not isinstance(text, str):
            text = text.decode(encoding=charset or "utf-8", errors="replace")
        return text

    def get_message(self):
        if self.validate():
            return {
                "sender": self.sender.data,
                "text": self.clean_text().strip(),
                "timestamp": self.timestamp.data or int(time.time()),
            }


class TelerivetForm(BaseHttpForm):
    """Helper form for validating incoming messages from a Telerivet-based SMS gateway.

    The parameters defined here are based on the Telerivet
    [Webhook API](http://telerivet.com/help/api/webhook/receiving)
    """

    id = wtforms.StringField()
    from_number = wtforms.StringField(validators=[wtforms.validators.data_required()])
    content = wtforms.StringField(validators=[wtforms.validators.data_required()])
    time_created = wtforms.IntegerField()

    def get_message(self):
        if self.validate():
            return {
                "sender": self.from_number.data,
                "text": self.content.data.replace("\x00", "").strip(),
                "timestamp": self.time_created.data,
            }


def retrieve_form(prefix, exclamation=False):
    """Retrieves a matching form for the given prefix.

    :param:`prefix` - The form prefix
    :param:`exclamation` - (optional) if specified, the search is limited to
                           incident forms
    :returns: a Form instance or None
    """
    current_events = services.events.overlapping_events(g.event)

    # find the first form that matches the prefix and optionally form type
    # for the current events
    query = models.Form.query.join(models.Form.events).filter(
        models.Event.id.in_(current_events.with_entities(models.Event.id)), models.Form.prefix.ilike(prefix)
    )

    if exclamation:
        query = query.filter(models.Form.form_type == "INCIDENT")

    form = query.with_entities(models.Form).first()

    return form
