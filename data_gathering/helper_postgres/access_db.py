from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String


class DatabaseAccess:
    def __init__(self, username, password, url, port, database):
        self.metadata = MetaData()
        self.base = declarative_base()
        self.engine = create_engine(f'postgresql+psycopg2://{username}:{password}@{url}:{port}/{database}')
        self.db_session = scoped_session(sessionmaker(autocommit=False, autoflush=True, bind=self.engine))

    def create_tables_in_database(self, data_class):
        db_object = self.convert_data_class_to_sql_object(data_class)

        self.base.metadata.create_all(self.engine)
        self.db_session.commit()

        return db_object

    def commit(self, initiated_data_class):
        self.db_session.add(initiated_data_class)

    def convert_data_class_to_sql_object(self, data_class):
        attr_dict = {
            "__tablename__": data_class.__name__.lower(),
            "__table_args__": {"schema": "public"},
            "id": Column(String, primary_key=True)
        }
        sql_alchemy_dict = {
            k.lower(): Column(v.metadata.get("sqlalchemy_type"))
            for k, v in data_class.__dataclass_fields__.items()
        }

        attr_dict.update(sql_alchemy_dict)

        return type(data_class.__name__, (self.base,), attr_dict)
