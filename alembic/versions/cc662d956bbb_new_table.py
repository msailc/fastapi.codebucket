"""new table

Revision ID: cc662d956bbb
Revises: d9dee0ee5366
Create Date: 2022-09-09 09:40:51.283069

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cc662d956bbb'
down_revision = 'd9dee0ee5366'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('assigned_team_needs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('team_need_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('assigned_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['team_need_id'], ['team_needs.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_assigned_team_needs_id'), 'assigned_team_needs', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_assigned_team_needs_id'), table_name='assigned_team_needs')
    op.drop_table('assigned_team_needs')
    # ### end Alembic commands ###
