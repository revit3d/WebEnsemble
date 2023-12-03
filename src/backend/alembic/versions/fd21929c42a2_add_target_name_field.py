"""add target_name field

Revision ID: fd21929c42a2
Revises: 5dec3a5a8cca
Create Date: 2023-12-03 15:15:12.224377

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fd21929c42a2'
down_revision = '5dec3a5a8cca'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ml_models', sa.Column('target_name', sa.String(), nullable=True))
    op.create_unique_constraint(None, 'ml_models', ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'ml_models', type_='unique')
    op.drop_column('ml_models', 'target_name')
    # ### end Alembic commands ###
