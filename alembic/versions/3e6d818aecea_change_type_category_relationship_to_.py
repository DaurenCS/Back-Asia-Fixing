"""Change Type.category relationship to uselist=False

Revision ID: 3e6d818aecea
Revises: ef425b7475e1
Create Date: 2024-05-21 18:33:10.881579

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3e6d818aecea'
down_revision: Union[str, None] = 'ef425b7475e1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
