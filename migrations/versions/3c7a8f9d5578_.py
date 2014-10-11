"""empty message

Revision ID: 3c7a8f9d5578
Revises: 4b36b8de9199
Create Date: 2014-10-12 01:00:37.715710

"""

# revision identifiers, used by Alembic.
revision = '3c7a8f9d5578'
down_revision = '4b36b8de9199'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('question', 'body',
               existing_type=sa.TEXT(),
               nullable=False)
    op.alter_column('question', 'slug',
               existing_type=sa.VARCHAR(length=300),
               nullable=False)
    op.alter_column('question', 'title',
               existing_type=sa.VARCHAR(length=240),
               nullable=False)
    op.alter_column('user', 'email',
               existing_type=sa.VARCHAR(length=100),
               nullable=False)
    op.alter_column('user', 'password',
               existing_type=sa.VARCHAR(length=1000),
               nullable=False)
    op.alter_column('user', 'username',
               existing_type=sa.VARCHAR(length=20),
               nullable=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'username',
               existing_type=sa.VARCHAR(length=20),
               nullable=True)
    op.alter_column('user', 'password',
               existing_type=sa.VARCHAR(length=1000),
               nullable=True)
    op.alter_column('user', 'email',
               existing_type=sa.VARCHAR(length=100),
               nullable=True)
    op.alter_column('question', 'title',
               existing_type=sa.VARCHAR(length=240),
               nullable=True)
    op.alter_column('question', 'slug',
               existing_type=sa.VARCHAR(length=300),
               nullable=True)
    op.alter_column('question', 'body',
               existing_type=sa.TEXT(),
               nullable=True)
    ### end Alembic commands ###
