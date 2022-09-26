# -*- coding: utf-8 -*-
from apollo.core import db
from apollo.factory import create_celery_app
from apollo.users.models import UserGeneratedFile

celery = create_celery_app()


@celery.task(bind=True)
def prune_generated_file(id: int) -> None:
    user_file = UserGeneratedFile.query.filter_by(id=id).first()
    if not user_file:
        return

    db.session.delete(user_file)
    db.session.commit()
