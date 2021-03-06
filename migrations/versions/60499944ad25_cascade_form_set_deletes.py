"""Cascade form set deletes

Revision ID: 60499944ad25
Revises: 840cf95b27b5
Create Date: 2019-01-22 17:36:29.028476

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '60499944ad25'
down_revision = '840cf95b27b5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('form_form_set_id_fkey', 'form', type_='foreignkey')
    op.create_foreign_key('form_form_set_id_fkey', 'form', 'form_set', ['form_set_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('form_form_set_id_fkey', 'form', type_='foreignkey')
    op.create_foreign_key('form_form_set_id_fkey', 'form', 'form_set', ['form_set_id'], ['id'])
    # ### end Alembic commands ###
