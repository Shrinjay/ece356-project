from client.domain.financial_data.domain import financial_data
from client.tests.common import assert_cols
from client.common.util import Variables
import pytest

@pytest.fixture
def stock_symbol():
    return 'RIV'


def test_get_financial_data_for_stock(stock_symbol):
    financial_data_columns = {"stockID", "Year", "Revenue", "RevenueGrowth", "CostofRevenue", "GrossProfit", "RDExpenses", "SGAExpenses", "OperatingExpenses", "OperatingIncome", "InterestExpense"}
    option = financial_data.options[0]
    df = option.run(kwargs={Variables.STOCK_SYMBOL.value: stock_symbol})

    assert_cols(df, financial_data_columns)


def test_get_financial_data():
    financial_data_columns = {"Symbol", "Year", "Revenue", "RevenueGrowth", "CostofRevenue", "GrossProfit", "RDExpenses", "SGAExpenses", "OperatingExpenses", "OperatingIncome", "InterestExpense"}
    option = financial_data.options[1]
    df = option.run()

    assert_cols(df, financial_data_columns)