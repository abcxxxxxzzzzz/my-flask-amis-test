"""empty message

Revision ID: d99df6b40a78
Revises: 6042e4756f9e
Create Date: 2023-02-03 13:15:00.221370

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd99df6b40a78'
down_revision = '6042e4756f9e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('url', table_name='admin_title')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('url', 'admin_title', ['url'], unique=False)
    # ### end Alembic commands ###