"""empty message

Revision ID: 36195abfacba
Revises: 
Create Date: 2024-12-17 13:30:39.401003

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '36195abfacba'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('players', schema=None) as batch_op:
        batch_op.drop_column('id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('players', schema=None) as batch_op:
        batch_op.add_column(sa.Column('id', sa.INTEGER(), nullable=True))

    # ### end Alembic commands ###
