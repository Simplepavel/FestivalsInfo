from Festival import app
from Festival.database.engine import create, drop
if __name__ == "__main__":
    create()
    app.run()
