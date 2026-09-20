## Running tests

pip install -r app/requirements.txt
pytest app/tests -v

Tests run against an isolated in-memory SQLite database and never touch
the PostgreSQL development database.

