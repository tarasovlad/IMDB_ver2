from sqlalchemy import *

engine = create_engine("postgresql+psycopg2://vlad:supervlad@94.228.122.247/coon_db", echo=True)


print(engine)