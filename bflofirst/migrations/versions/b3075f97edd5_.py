"""empty message

Revision ID: b3075f97edd5
Revises: None
Create Date: 2016-11-03 13:12:45.916557

"""

# revision identifiers, used by Alembic.
revision = 'b3075f97edd5'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('listings', sa.Column('mailed', sa.Boolean(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('listings', 'mailed')
    ### end Alembic commands ###
