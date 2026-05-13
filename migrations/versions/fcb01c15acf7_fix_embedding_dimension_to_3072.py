"""fix_embedding_dimension_to_3072

Revision ID: fcb01c15acf7
Revises: b0fb7ed81a72
Create Date: 2026-05-13 13:22:38.057944

"""
from typing import Sequence, Union

from alembic import op

revision: str = 'fcb01c15acf7'
down_revision: Union[str, Sequence[str], None] = 'b0fb7ed81a72'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        "ALTER TABLE document_chunks "
        "ALTER COLUMN embedding TYPE vector(3072) "
        "USING embedding::text::vector(3072)"
    )


def downgrade() -> None:
    op.execute(
        "ALTER TABLE document_chunks "
        "ALTER COLUMN embedding TYPE vector(768) "
        "USING embedding::text::vector(768)"
    )
