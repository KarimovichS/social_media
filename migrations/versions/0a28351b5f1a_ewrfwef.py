"""ewrfwef

Revision ID: 0a28351b5f1a
Revises: c5c359645f48
Create Date: 2024-04-20 20:13:11.465511

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0a28351b5f1a'
down_revision: Union[str, None] = 'c5c359645f48'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('followers', sa.Column('is_following', sa.Boolean(), nullable=False))
    op.alter_column('followers', 'follower_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('followers', 'follower_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.drop_column('followers', 'is_following')
    # ### end Alembic commands ###
