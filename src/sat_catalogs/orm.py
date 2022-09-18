"""Database interactions"""

from enum import Enum
from sqlalchemy import Table, select
from sqlalchemy.engine import Engine, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

Base = declarative_base()


class SatModel(Enum):
    """Table names for models"""

    FORM_OF_PAYMENT = "cfdi_40_formas_pago"
    UNIT_OF_MEASURE = "cfdi_40_claves_unidades"
    TAX_SYSTEM = "cfdi_40_regimenes_fiscales"


def get_db_engine(db_path: str) -> Engine:
    """Creates a new SQLAlchemy Engine instance from path

    Args:
        db_path (str): Path to SQLite database

    Returns:
        Engine: Connection to database
    """
    return create_engine(f"sqlite:///{db_path}", echo=False, future=True)


def get_model(model: SatModel, engine: Engine):
    """Creates a Model class to bind for the model object

    Args:
        model (SatModel): Model name to get
        engine (Engine): Connection to database

    Raises:
        KeyError: If model name is not supported

    Returns:
        Model: Model instance binded to database table
    """

    class Model(Base):
        """Common model class"""

        __table__ = Table(model.value, Base.metadata, autoload_with=engine)

    return Model


def get_record_scalars(model: SatModel, db_path: str):
    """Connect to database and retrieve results as scalars

    Args:
        model (SatModel): Model of the object to retrieve
        db_path (str): Path to SQLite database

    Returns:
        ScalarResult: All table record objects
    """

    engine = get_db_engine(db_path)
    session = Session(engine)
    model_class = get_model(model, engine)
    results = select(model_class)
    return session.scalars(results)
