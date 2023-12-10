from enum import Enum
from typing import List
import pandas as pd
import tabulate
import datetime
import sqlalchemy

class Variables(Enum):
    STOCK_SYMBOL = 'stock_symbol'
    RATING = 'rating'
    ANALYST = 'analyst_id'
    STOCK_SYMBOL1 = 'stock_symbol1'
    STOCK_SYMBOL2 = 'stock_symbol2'
    DATE = 'date'
    PRICE_PER_SHARE = 'price_per_share'
    NUM_SHARES = 'num_shares'
    FILING_TYPE = 'filing_type'
    TARGET_PRICE = 'target_price'


class AnalystRating(Enum):
    BUY = 'BUY'
    SELL = 'SELL'
    HOLD = 'HOLD'
    UNDERPERFORM = 'UNDERPERFORM'
    OUTPERFORM = 'OUTPERFORM'

class Query:
    def __init__(self, variables: List[Variables], fn):
        self.variables = variables
        self.fn = fn


class Option:
    def __init__(self, id: str, query: Query):
        self.id = id
        self.query = query

    def run(self):
        kwargs = {}
        variable_parser = VariableParser()

        for variable in self.query.variables:
            varname = variable.value
            var = input(f"Enter {varname}:")
            parsed_var = variable_parser.parse(variable, var)
            kwargs[varname] = parsed_var

        df = self.query.fn(**kwargs)
        self.print(df)
        return df

    def print(self, df: pd.DataFrame):
        print(f"==================Results==================")
        print(tabulate(df, headers='keys', tablefmt='psql'))
        print(f"==================End of Results==================")


class Domain:
    def __init__(self, domain_name: str, options: List[Option]):
        self.domain_name = domain_name
        self.options = options

    def run(self):
        num_options = len(self.options)
        print(f"Select an option:")

        for i in range(len(self.options)):
            option = self.options[i]
            print(f"Press {i} to {option.id}")

        option = int(input("Select an option or enter -1 to exit:"))

        if option == -1:
            return

        if option > num_options:
            print("Invalid option selected")
            return

        selected_option = self.options[option]
        selected_option.run()


class Client:
    def __init__(self, domains: List[Domain]):
        self.domains = domains

    def run(self):
        while True:

            num_options = len(self.domains)

            for i in range(len(self.domains)):
                domain = self.domains[i]
                print(f"Press {i} for {domain.domain_name}")

            option = int(input("Select an option or enter -1 to exit:"))

            if option == -1:
                return

            if option > num_options:
                print("Invalid option selected")
                return

            selected_option = self.domains[option]
            selected_option.run()


def get_db_url():
    return sqlalchemy.URL.create(
        "mysql+pymysql",
        username="root",
        password="",
        host="localhost",
        port=3306,
        database="team99"
    )


class VariableParser:
    @staticmethod
    def _parse_int(str: str):
        return int(str)

    @staticmethod
    def _parse_date(str: str):
        return datetime.datetime.strptime(str, "%Y-%m-%d")

    parsers = {
        Variables.ANALYST: _parse_int,
        Variables.DATE: _parse_date
    }

    def parse(self, variable: Variables, val: str):
        if variable in self.parsers:
            return self.parsers[variable](val)
        return val


def run_insert_query(query: str) -> int:
    db_url = get_db_url()
    engine = sqlalchemy.engine.create_engine(url=db_url)
    connection = engine.connect()
    result = connection.execute(sqlalchemy.text(query))
    new_id = result.lastrowid

    connection.commit()
    connection.close()
    return new_id


def run_select_query(query: str) -> pd.DataFrame:
    db_url = get_db_url()
    engine = sqlalchemy.engine.create_engine(url=db_url)
    connection = engine.connect()
    df = pd.read_sql(sql=query, con=connection)

    connection.close()
    return df