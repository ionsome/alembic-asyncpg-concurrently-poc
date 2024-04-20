import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from poc_setup import apply_migrations, target_metadata, do_run_migrations
from sqlalchemy import text
import alembic
from sqlalchemy import create_engine

sync_engine = create_engine(
    'postgresql://user:password@127.0.0.1:5432/test_db',
    echo=True,
)

async_engine = create_async_engine(
    'postgresql+asyncpg://user:password@127.0.0.1:5432/test_db',
    echo=True,
)

async def run_migrations_online() -> None:
    with sync_engine.connect() as connection1:
        async with async_engine.connect() as connection2:
            connection1.execute(text('SELECT 1;'))
            await connection2.run_sync(
                do_run_migrations,
                alembic.context,  # type: ignore [arg-type]
                target_metadata
            )


if __name__ == '__main__':
    asyncio.run(apply_migrations(run_migrations_online))
