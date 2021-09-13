"""remove participant groups

Revision ID: c4166678fb79
Revises: 5c885dc2badc
Create Date: 2021-09-10 17:30:23.965849

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "c4166678fb79"
down_revision = "5c885dc2badc"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("participant_groups_participants")
    op.drop_table("participant_group")
    op.drop_table("participant_group_type")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "participant_groups_participants",
        sa.Column(
            "group_id", sa.INTEGER(), autoincrement=False, nullable=False
        ),
        sa.Column(
            "participant_id", sa.INTEGER(), autoincrement=False, nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["group_id"],
            ["participant_group.id"],
            name="participant_groups_participants_group_id_fkey",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["participant_id"],
            ["participant.id"],
            name="participant_groups_participants_participant_id_fkey",
            ondelete="CASCADE",
        ),
    )
    op.create_table(
        "participant_group_type",
        sa.Column(
            "id",
            sa.INTEGER(),
            server_default=sa.text(
                "nextval('participant_group_type_id_seq'::regclass)"
            ),
            nullable=False,
        ),
        sa.Column("name", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column(
            "participant_set_id",
            sa.INTEGER(),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "uuid", postgresql.UUID(), autoincrement=False, nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["participant_set_id"],
            ["participant_set.id"],
            name="participant_group_type_participant_set_id_fkey",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name="participant_group_type_pkey"),
        postgresql_ignore_search_path=False,
    )
    op.create_table(
        "participant_group",
        sa.Column("id", sa.INTEGER(), nullable=False),
        sa.Column("name", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column(
            "group_type_id", sa.INTEGER(), autoincrement=False, nullable=False
        ),
        sa.Column(
            "participant_set_id",
            sa.INTEGER(),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "uuid", postgresql.UUID(), autoincrement=False, nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["group_type_id"],
            ["participant_group_type.id"],
            name="participant_group_group_type_id_fkey",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["participant_set_id"],
            ["participant_set.id"],
            name="participant_group_participant_set_id_fkey",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name="participant_group_pkey"),
    )
    # ### end Alembic commands ###
