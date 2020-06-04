"""migrate QA expressions

Revision ID: 1e17be41a449
Revises: 32263b7ab47e
Create Date: 2020-05-23 18:00:25.856539

"""
from alembic import op
import sqlalchemy as sa
from apollo.formsframework.models import Form
from apollo.submissions.qa import query_builder as qb

# revision identifiers, used by Alembic.
revision = '1e17be41a449'
down_revision = '32263b7ab47e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    fetch_query = sa.sql.text(
        "SELECT id, quality_checks FROM form WHERE quality_checks IS NOT NULL OR quality_checks != 'null'::jsonb;")  # noqa
    form_table = Form.__table__
    connection = op.get_bind()
    for form_id, quality_checks in connection.execute(fetch_query).fetchall():
        if not quality_checks:
            continue
        for quality_check in quality_checks:
            if 'expression' not in quality_check:
                quality_check['expression'] = qb.build_expression(
                    quality_check)
                quality_check.pop('criteria')
        statement = form_table.update().where(
            form_table.c.id == form_id
        ).values(quality_checks=quality_checks)
        op.execute(statement)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    # ### end Alembic commands ###
    pass
