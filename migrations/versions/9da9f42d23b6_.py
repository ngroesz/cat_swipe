"""empty message

Revision ID: 9da9f42d23b6
Revises: 44a74667e4a9
Create Date: 2019-01-14 14:24:04.351908

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9da9f42d23b6'
down_revision = '44a74667e4a9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('persons', sa.Column('name', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('persons', 'name')
    # ### end Alembic commands ###
