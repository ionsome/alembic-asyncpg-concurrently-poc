from collections.abc import Awaitable
from typing import Any, Callable

import sqlalchemy as sa
from alembic.runtime.environment import EnvironmentContext
from sqlalchemy.engine.base import Connection

from alembic import config as alembic_config
from alembic.runtime.migration import RevisionStep
from alembic.script import ScriptDirectory
from sqlalchemy import MetaData


ALEMBIC_CFG = alembic_config.Config('alembic.ini')

target_metadata = metadata = MetaData()


def do_run_migrations(
    connection: Connection,
    context: EnvironmentContext,
    metadata: sa.MetaData,
) -> None:
    context.configure(
        connection=connection,
        target_metadata=metadata,
        transaction_per_migration=True,
    )
    with context.begin_transaction():
        context.run_migrations()

async def apply_migrations(
    run_migrations_online: Callable[[], Awaitable[Any]],
    revision: str = 'head',
) -> None:
    _alembic_cfg = ALEMBIC_CFG
    script = ScriptDirectory.from_config(_alembic_cfg)

    def upgrade(
        rev: str | tuple[str, ...] | None,
        context: EnvironmentContext,
    ) -> list[RevisionStep]:
        return script._upgrade_revs(revision, rev)  # type: ignore [arg-type] 

    with EnvironmentContext(
        _alembic_cfg,
        script,
        fn=upgrade,
        starting_rev=None,
        destination_rev=revision,
    ):
        await run_migrations_online()

