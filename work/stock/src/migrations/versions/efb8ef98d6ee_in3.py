"""in3

Revision ID: efb8ef98d6ee
Revises: 
Create Date: 2020-08-24 16:10:01.703349

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'efb8ef98d6ee'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('groups',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('stockgroups',
    sa.Column('stock_id', sa.Integer(), nullable=True),
    sa.Column('group_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['group_id'], ['groups.id'], ),
    sa.ForeignKeyConstraint(['stock_id'], ['stocks.id'], )
    )
    op.create_index(op.f('ix_stocks_ts_code'), 'stocks', ['ts_code'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_stocks_ts_code'), table_name='stocks')
    op.drop_table('stockgroups')
    op.drop_table('groups')
    # ### end Alembic commands ###