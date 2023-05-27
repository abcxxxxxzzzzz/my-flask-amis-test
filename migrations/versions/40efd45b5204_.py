"""empty message

Revision ID: 40efd45b5204
Revises: d99df6b40a78
Create Date: 2023-02-03 13:31:37.803730

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '40efd45b5204'
down_revision = 'd99df6b40a78'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('admin_title', sa.Column('upload_tag', sa.String(length=255), nullable=True, comment='上传标签'))
    op.alter_column('admin_title', 'tag',
               existing_type=mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=255),
               comment='爬虫标签',
               existing_comment='标签',
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('admin_title', 'tag',
               existing_type=mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=255),
               comment='标签',
               existing_comment='爬虫标签',
               existing_nullable=True)
    op.drop_column('admin_title', 'upload_tag')
    # ### end Alembic commands ###