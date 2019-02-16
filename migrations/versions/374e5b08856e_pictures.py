"""pictures

Revision ID: 374e5b08856e
Revises: 68c9db0467ae
Create Date: 2019-02-12 09:42:05.766817

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '374e5b08856e'
down_revision = '68c9db0467ae'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'profile_pic',
               existing_type=sa.VARCHAR(length=20),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'profile_pic',
               existing_type=sa.VARCHAR(length=20),
               nullable=True)
    # ### end Alembic commands ###
