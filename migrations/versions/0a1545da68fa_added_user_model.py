"""added user model

Revision ID: 0a1545da68fa
Revises: 
Create Date: 2022-03-03 16:59:19.308028

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0a1545da68fa'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('client',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('publicId', sa.String(length=36), nullable=True),
    sa.Column('firstName', sa.String(length=20), nullable=False),
    sa.Column('lastName', sa.String(length=20), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('passwordHash', sa.String(length=100), nullable=False),
    sa.Column('registeredOn', sa.DateTime(), nullable=True),
    sa.Column('lastLogin', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('firstName'),
    sa.UniqueConstraint('lastName'),
    sa.UniqueConstraint('publicId')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('client')
    # ### end Alembic commands ###
