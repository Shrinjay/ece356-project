from client.domain.bankruptices.domain import bankruptcies
from client.tests.common import assert_cols, delete_row
from client.common.util import Variables
import pytest

@pytest.fixture
def stock_symbol():
    return 'RIV'

def test_get_all_bankruptices():
    columns = {"Symbol", "FilingType", "Date"}
    option = bankruptcies.options[0]
    df = option.run()

    assert_cols(df, columns)


def test_insert_bankruptcy(stock_symbol):
    option = bankruptcies.options[1]
    kwargs = {
        Variables.STOCK_SYMBOL.value: stock_symbol,
        Variables.DATE.value: '2022-04-04',
        Variables.FILING_TYPE.value: 'Chapter 11'
    }

    df = option.run(kwargs=kwargs)
    inserted_row = df.head(1)

    id = inserted_row['ID'].item()
    filing_type = inserted_row['FilingType'].item()

    delete_row(id, 'Bankruptcy')

    assert filing_type == 'Chapter 11'