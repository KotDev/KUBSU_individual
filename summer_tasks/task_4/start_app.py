from summer_tasks.task_4.app.view import app
from database import Base, engine

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    app.run(host="127.0.0.1", port=8000, debug=True)