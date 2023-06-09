"""empty message

Revision ID: 3c29fa634301
Revises: eb6282c85528
Create Date: 2023-01-24 14:06:18.549302

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3c29fa634301'
down_revision = 'eb6282c85528'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('admin_title', sa.Column('status', sa.Integer(), nullable=True, comment='状态'))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('admin_title', 'status')
    # ### end Alembic commands ###
