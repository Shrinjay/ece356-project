from client.domain.trading_data.domain import trading_data
from client.tests.common import assert_cols
from client.common.util import Variables
import pytest

@pytest.fixture
def stock_id():
    return 1


@pytest.fixture
def stock_symbol():
    return 'RIV'

@pytest.fixture
def stock_id2():
    return 2

@pytest.fixture
def stock_symbol2():
    return "ANTE"


def test_get_trading_data_for_stock(stock_id, stock_symbol):
    # We want to assert that the correct columns are there
    trading_data_cols = {'stockID', 'Date', 'Volume', 'Open', 'High', 'Low', 'Close', 'AdjustedClose'}

    option = trading_data.options[0]
    df = option.run(kwargs={Variables.STOCK_SYMBOL.value: stock_symbol})

    assert_cols(df, trading_data_cols)


def test_compare_stock_trading_data(stock_symbol, stock_symbol2, stock_id, stock_id2):
    # s1.Date as Date, s1.Volume as first_stock_volume, s1.Close as first_stock_price, s2.Volume as second_stock_volume, s2.Close as second_stock_price
    compare_cols = {'Date', 'stockID', 'otherStockID', 'first_stock_volume', 'first_stock_price', 'second_stock_volume', 'second_stock_price'}

    option = trading_data.options[1]
    df = option.run(kwargs={Variables.STOCK_SYMBOL1.value: stock_symbol, Variables.STOCK_SYMBOL2.value: stock_symbol2})

    assert_cols(df, compare_cols)