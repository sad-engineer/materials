"""Add standard_id to chemical_composition

Revision ID: dec204b8f6d2
Revises: 
Create Date: 2024-11-26 16:05:42.661082

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dec204b8f6d2'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Используем batch mode для добавления нового столбца и внешнего ключа в SQLite
    with op.batch_alter_table('chemical_composition', schema=None) as batch_op:
        # Добавляем новый столбец standard_id в таблицу chemical_composition
        batch_op.add_column(sa.Column('standard_id', sa.Integer(), nullable=True))
        # Добавляем внешний ключ, связывающий standard_id с таблицей standards
        batch_op.create_foreign_key(
            'fk_chemical_composition_standard',  # Название внешнего ключа
            'standards',                         # Имя таблицы, на которую ссылаемся
            ['standard_id'],                     # Поле в исходной таблице
            ['id']                               # Поле в целевой таблице
        )


def downgrade() -> None:
    # Используем batch mode для удаления внешнего ключа и столбца в случае отката миграции
    with op.batch_alter_table('chemical_composition', schema=None) as batch_op:
        # Удаляем внешний ключ
        batch_op.drop_constraint('fk_chemical_composition_standard', type_='foreignkey')
        # Удаляем столбец standard_id
        batch_op.drop_column('standard_id')
