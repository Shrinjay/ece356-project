import pandas as pd
from typing import Set
from client.common.util import get_db_url
import sqlalchemy

def assert_cols(df, true_col_set):
    col_set = set(df.columns.values)

    assert col_set == true_col_set

def assert_column(df, colname, allowed_vals: Set):
    col: pd.Series = df[colname]

    assert col.map(lambda v: v in allowed_vals).all()

def delete_row(id, table):
    db_url = get_db_url()
    engine = sqlalchemy.engine.create_engine(url=db_url)
    connection = engine.connect()
    connection.execute(sqlalchemy.text(f"DELETE FROM {table} where ID={id};"))
    connection.commit()
    connection.close()