from client.domain.analyst_ratings.domain import analyst_ratings
from client.tests.common import assert_cols, delete_row
from client.common.util import Variables
from client.common.auth import auth_manager
import pytest

@pytest.fixture
def stock_symbol():
    return 'RIV'

@pytest.fixture()
def stock_id():
    return 1

def test_get_all_analysts():
    columns = {"AnalystID", "FirmName"}
    option = analyst_ratings.options[0]
    df = option.run()

    assert_cols(df, columns)

def test_get_all_ratings_for_analyst():
    columns = {"Symbol", "Date", "Rating", "TargetPrice"}
    option = analyst_ratings.options[1]
    df = option.run(kwargs={Variables.ANALYST.value: '1'})

    assert_cols(df, columns)
def test_get_ratings(stock_symbol):
    columns = {"Date", "Rating", "Name", "AnalystID", "FirmName", "TargetPrice"}
    option = analyst_ratings.options[2]
    df = option.run(kwargs={Variables.STOCK_SYMBOL.value: stock_symbol})

    assert_cols(df, columns)

def test_get_ratings_by_rating():
    columns = {"Date", "Rating", "Name", "AnalystID", "FirmName", "TargetPrice"}
    option = analyst_ratings.options[3]
    df = option.run(kwargs={Variables.STOCK_SYMBOL.value: stock_symbol, Variables.RATING.value: 'Buy'})

    assert_cols(df, columns)

def test_insert_rating(stock_symbol, stock_id):
    option = analyst_ratings.options[4]
    auth_manager.current_user_id = 1
    # Variables.STOCK_SYMBOL, Variables.RATING, Variables.TARGET_PRICE
    kwargs = {
        Variables.STOCK_SYMBOL.value: stock_symbol,
        Variables.RATING.value: 'BUY',
        Variables.TARGET_PRICE.value: 0.00
    }

    df = option.run(kwargs=kwargs)
    inserted_row = df.head(1)

    id = inserted_row['ID'].item()
    stock_id_in_data = inserted_row['stockID'].item()
    analyst_id = inserted_row['analystID'].item()
    rating = inserted_row['Rating'].item()
    target_price = inserted_row['TargetPrice'].item()

    delete_row(id, 'AnalystRating')

    assert stock_id == stock_id_in_data
    assert analyst_id == 1
    assert rating == 'Buy'
    assert target_price == 0.00