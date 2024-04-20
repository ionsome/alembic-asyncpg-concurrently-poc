import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '67fe424a1454'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'table_1',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('data', sa.String(), nullable=False),
    )
    
    with op.get_context().autocommit_block():
        op.execute('INSERT INTO table_1 VALUES(1, \'aboba\')') # works
        op.execute('SELECT 1') # works

        op.execute('CREATE INDEX CONCURRENTLY ix_1 ON table_1 (data)') # stucks
        op.execute('SELECT 1') # not reached

def downgrade() -> None:
    op.drop_table('table_1')
