This is a Point of Sale (POS) application I built with FastAPI. The system is designed for a general retail business, such as a supermarket, mini-mart, or convenience store, where a cashier serves walk-in and registered customers, tracks stock levels across multiple product categories and suppliers, and needs a clear, auditable record of every sale from checkout through payment and receipt.


## Running tests

pip install -r app/requirements.txt
pytest app/tests -v

Tests run against an isolated in-memory SQLite database and never touch
the PostgreSQL development database.




