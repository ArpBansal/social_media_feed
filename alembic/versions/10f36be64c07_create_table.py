"""create table

Revision ID: 10f36be64c07
Revises: 
Create Date: 2024-02-02 21:25:48.106724

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '10f36be64c07'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True, index=True),
    sa.Column('title', sa.String(), nullable=False))


def downgrade():
    op.drop_table('posts')
