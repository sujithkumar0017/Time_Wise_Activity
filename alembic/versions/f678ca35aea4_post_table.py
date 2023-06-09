"""post table

Revision ID: f678ca35aea4
Revises: f9466662ac1b
Create Date: 2023-05-22 13:00:10.874742

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import text

# revision identifiers, used by Alembic.
revision = 'f678ca35aea4'
down_revision = 'f9466662ac1b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'post',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('post_name', sa.String(length=50), nullable=False),
        sa.Column('content', sa.String(length=255), nullable=False),
        sa.Column('post_created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=text('now()')),
        sa.Column('owner_id',sa.Integer(),sa.ForeignKey("users.id",ondelete="CASCADE"),nullable=False)
)


def downgrade() -> None:
    op.drop_table('post')
