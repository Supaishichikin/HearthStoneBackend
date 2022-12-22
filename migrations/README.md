## LOCAL

- Make changes u want to the models ( add another field, override existing fields types...) or adding new models. 
- `export DATABASE_URL=THE_DB_URL`
- `alembic revision --autogenerate -m "MIGRATIONS_VERSION_NAME(e.g: add full name field to user table)"` => It should create all the tables
- In the folder migrations/versions, a new version will be added automatically. Make sure it does correspond to the changes you did in the models, and make changes if necessary.  
- `alembic upgrade head` => It should create all the tables (including alembic_version which will have the latest version_num)