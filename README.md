# FastAPI Server 

This repository attempts to replicate best practices in FastAPI from [this](https://github.com/zhanymkanov/fastapi-best-practices) repository.

### Setup Alembic  
- Navigate to your project directory, and generate alembic files by running the ff. command on your terminal: 
```bash
alembic init alembic 
```
- Navigate to `alembic.ini` on the project's root folder, and change `sqlalchemy.url` to your database url. 
- Update alembic/env.py
  - Import the `Base` variable from `src/database/database.py` 
  - Change the `target_metadata` variable to `Base.metadata`  
- Update alembic/script.py.mako 
  - Add `import sqlmodel` under the imports section
- Alembic Commands
  - `alembic revision --autogenerate -m <message>` This will generate a Python script to handle migrations. 
  - `alembic upgrade head` This will run the upgrade function and apply the changes in `models.py` into the database. 
  - `alembic downgrade -1` This will downgrade the database to the previous version