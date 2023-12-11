import datetime

from client.domain.ipo.domain import ipo
from client.tests.common import assert_cols, delete_row
from client.common.util import Variables
import pytest


@pytest.fixture
def stock_symbol():
    return 'RIV'


def test_get_ipo(stock_symbol):
    ipo_columns = {"PricePerShare", "NumShares"}
    option = ipo.options[0]
    df = option.run(kwargs={Variables.STOCK_SYMBOL.value: stock_symbol})

    assert_cols(df, ipo_columns)


def test_get_all_ipo(stock_symbol):
    ipo_columns = {"Symbol", "PricePerShare", "NumShares", "Date"}
    option = ipo.options[1]
    df = option.run()

    assert_cols(df, ipo_columns)

def test_insert_ipo(stock_symbol):
    option = ipo.options[2]
    kwargs = {
        Variables.STOCK_SYMBOL.value: stock_symbol,
        Variables.DATE.value: '2022-04-04',
        Variables.PRICE_PER_SHARE.value: 0.00,
        Variables.NUM_SHARES.value: 0
    }

    df = option.run(kwargs=kwargs)
    inserted_row = df.head(1)

    id = inserted_row['ID'].item()
    price_per_share = inserted_row['PricePerShare'].item()
    num_shares = inserted_row['NumShares'].item()

    delete_row(id, 'IPO')

    assert num_shares == 0
    assert price_per_share == 0.00