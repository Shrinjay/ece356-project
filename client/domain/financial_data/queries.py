from client.common.util import Query, Variables
from client.common.util import run_select_query


def _get_financial_data():
    query = f"""
    select Stock.Symbol, FD.Year, FD.Revenue, FD.RevenueGrowth, FD.CostofRevenue, FD.GrossProfit, FD.RDExpenses, FD.SGAExpenses, FD.OperatingExpenses, FD.OperatingIncome, FD.InterestExpense
    from Stock inner join FinancialData as FD on Stock.ID = FD.stockID;
    """

    return run_select_query(query)

get_financial_data = Query(
    variables=[],
    fn=_get_financial_data
)


#
# -- get Financial data for a particular stock
# select Year, Revenue, RevenueGrowth, CostofRevenue, GrossProfit, RDExpenses, SGAExpenses, OperatingExpenses, OperatingIncome, InterestExpense
# from FinancialData
# where stockID = (select ID from Stock where Symbol = '{stock_symbol}');
def _get_financial_data_for_stock(stock_symbol: str):
    query = f"""   
    select Year, Revenue, RevenueGrowth, CostofRevenue, GrossProfit, RDExpenses, SGAExpenses, OperatingExpenses, OperatingIncome, InterestExpense
    from FinancialData
    where stockID = (select ID from Stock where Symbol = '{stock_symbol}');
    """

    return run_select_query(query)

get_financial_data_for_stock = Query(
    variables=[Variables.STOCK_SYMBOL],
    fn=_get_financial_data_for_stock
)
