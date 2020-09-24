# -*- coding: utf-8 -*-
import base64
import io
import json
import zlib
from urllib.parse import urljoin

import qrcode
from flask import url_for


def make_message_text(form, participant, data):
    message_body = f'{form.prefix} {participant.participant_id}'

    for tag in form.tags:
        field_value = data.get(tag)
        if field_value is None:
            continue

        field = form.get_field_by_tag(tag)
        if field.get('type') == 'multiselect':
            value_rep = ''.join(str(i) for i in sorted(field_value))
        else:
            value_rep = field_value

        message_body += f' {tag}{value_rep}'

    return message_body


def generate_qr_code(participant=None):
    settings = {
        'general': {
            'server_url': urljoin(
                url_for('dashboard.index', _external=True), 'xforms'
            )
        },
        'admin': {}
    }

    if participant:
        settings['general'].update(
            username=participant.participant_id,
            password=participant.password
        )

    json_bytes = json.dumps(settings).encode('UTF-8')
    compressed_json = zlib.compress(json_bytes)

    qr_code = qrcode.QRCode(
        version=1, error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10, border=4
    )
    qr_code.add_date(base64.b64encode(compressed_json))
    qr_code.make()

    img_buffer = io.BytesIO()
    img = qr_code.make_image(fill_color='black', back_color='white')
    img.save(img_buffer, format='PNG')
    img_buffer.seek(0)

    return img_buffer.getvalue()
