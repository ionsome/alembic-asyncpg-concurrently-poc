# Asyncpg is breaking alembic autocommit mode

Description
---
Creating postgresql index concurrently  in migrations using `op.get_context().autocommit_block()` may cause a program stuck if you have opened asyncpg transaction.

The repository contains 4 examples. The first two use an async connection before applying migrations and have the problem, seconds two use an sync connection and do not have the problem. 

python 3.10
sqlalchemy 2.0.29
alembic 1.13.1
asyncpg 0.29.0
psycopg2 2.9.9

How to reproduce
---

```
docker-compose up -d
python3 example1_async_apply.py
# OR
python3 example2_sync_apply.py  # Be carefull, it ignores Ctrl + C
```
