"""add location groups

Revision ID: 5c885dc2badc
Revises: e00e521a0434
Create Date: 2021-08-04 09:07:10.486951

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '5c885dc2badc'
down_revision = 'e00e521a0434'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('location_group',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('location_set_id', sa.Integer(), nullable=False),
        sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=False),
        sa.ForeignKeyConstraint(['location_set_id'], ['location_set.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('locations_groups',
        sa.Column('location_id', sa.Integer(), nullable=False),
        sa.Column('location_group_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['location_group_id'], ['location_group.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['location_id'], ['location.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('location_id', 'location_group_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('locations_groups')
    op.drop_table('location_group')
    # ### end Alembic commands ###
