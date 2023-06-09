"""user_activity

Revision ID: e9e52f4532ae
Revises: f678ca35aea4
Create Date: 2023-05-24 17:39:15.941730

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import text

# revision identifiers, used by Alembic.
revision = 'e9e52f4532ae'
down_revision = 'f678ca35aea4'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'user_activity',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False,autoincrement=True),
        sa.Column('entity_id', sa.Integer(), sa.ForeignKey("post.id", ondelete="CASCADE"), nullable=False),
        sa.Column('entity_type',sa.String(length=255),default="Post"),
        sa.Column('actor', sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column('action',sa.String(length=255),default="Create"),
        sa.Column('raw_data',sa.JSON),
        sa.Column('logged_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=text('now()')))


def downgrade() -> None:
    op.drop_table('user_activity')

