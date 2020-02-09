"""remove Sample model

Revision ID: 09ffec04da8f
Revises: 3f4fcfd3d063
Create Date: 2020-02-09 10:31:16.935212

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '09ffec04da8f'
down_revision = '3f4fcfd3d063'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('samples_locations')
    op.drop_table('sample')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sample',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('sample_id_seq'::regclass)"), nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('location_set_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('uuid', postgresql.UUID(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['location_set_id'], ['location_set.id'], name='sample_location_set_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name='sample_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('samples_locations',
    sa.Column('sample_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('location_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['location_id'], ['location.id'], name='samples_locations_location_id_fkey', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['sample_id'], ['sample.id'], name='samples_locations_sample_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('sample_id', 'location_id', name='samples_locations_pkey')
    )
    # ### end Alembic commands ###
