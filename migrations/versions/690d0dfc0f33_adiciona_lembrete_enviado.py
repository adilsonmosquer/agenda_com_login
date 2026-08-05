"""Adiciona lembrete_enviado

Revision ID: 690d0dfc0f33
Revises: 362646603920
Create Date: 2026-08-05 14:45:55.729581

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "690d0dfc0f33"
down_revision = "362646603920"
branch_labels = None
depends_on = None


def upgrade():

    with op.batch_alter_table(
        "cronograma_itens",
        schema=None,
    ) as batch_op:

        batch_op.add_column(

            sa.Column(

                "lembrete_enviado",

                sa.Boolean(),

                nullable=False,

                server_default=sa.false(),

            )

        )


def downgrade():

    with op.batch_alter_table(
        "cronograma_itens",
        schema=None,
    ) as batch_op:

        batch_op.drop_column(
            "lembrete_enviado"
        )