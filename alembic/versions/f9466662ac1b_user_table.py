"""user table

Revision ID: f9466662ac1b
Revises: 
Create Date: 2023-05-22 12:13:58.710052

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import text

# revision identifiers, used by Alembic.
revision = 'f9466662ac1b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True,nullable=False,autoincrement=True),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('email',sa.String,nullable=False),
        sa.Column('phone',sa.Integer,nullable=False),
        sa.Column('password',sa.String,nullable=False),
        sa.Column('created_at',sa.TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    )


def downgrade() -> None:
    op.drop_table('users')


# op.create_table(
#     'users',
#     sa.Column('id', sa.Integer(), primary_key=True),
#     sa.Column('name', sa.String(length=255), nullable=False),
# )