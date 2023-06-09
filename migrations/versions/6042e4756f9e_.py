"""empty message

Revision ID: 6042e4756f9e
Revises: 7ee1e614c259
Create Date: 2023-02-03 12:05:58.647796

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '6042e4756f9e'
down_revision = '7ee1e614c259'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('admin_title', sa.Column('keywords', sa.Text(), nullable=True, comment='网站关键词'))
    op.add_column('admin_title', sa.Column('description', sa.Text(), nullable=True, comment='网站描述'))
    op.alter_column('admin_title', 'title',
               existing_type=mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=10000),
               comment='网站标题',
               existing_comment='标题',
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('admin_title', 'title',
               existing_type=mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=10000),
               comment='标题',
               existing_comment='网站标题',
               existing_nullable=True)
    op.drop_column('admin_title', 'description')
    op.drop_column('admin_title', 'keywords')
    # ### end Alembic commands ###
