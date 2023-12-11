from client.common.util import run_select_query
from client.common.util import Query, Variables

def _get_trading_data_for_stock(stock_symbol: str):
    query = f"""  
    select stockID, Date, Volume, Open, High, Close, Low, AdjustedClose from
    TradingData where stockID = (select ID from Stock where Symbol = '{stock_symbol}');
    """

    return run_select_query(query)

get_trading_data_for_stock = Query(
    variables=[Variables.STOCK_SYMBOL],
    fn=_get_trading_data_for_stock
)

#
# -- compare two stocks side by side
# select s1.Date as Date, s1.Volume as first_stock_volume, s1.Close as first_stock_price, s2.Volume as second_stock_volume, s2.Close as second_stock_price
# from TradingData as s1 inner join TradingData as s2 on s1.Date = s2.Date
# where s1.stockID = (select ID from Stock where Symbol = '{stock_symbol1}') and
# s2.stockID = (select ID from Stock where Symbol = '{stock_symbol2}');


def _compare_stock_trading_data(stock_symbol1: str, stock_symbol2: str):
    query = f"""
    select s1.Date as Date, s1.stockID as stockID, s2.stockID as otherStockID, s1.Volume as first_stock_volume, s1.Close as first_stock_price, s2.Volume as second_stock_volume, s2.Close as second_stock_price
    from TradingData as s1 inner join TradingData as s2 on s1.Date = s2.Date
    where s1.stockID = (select ID from Stock where Symbol = '{stock_symbol1}') and
    s2.stockID = (select ID from Stock where Symbol = '{stock_symbol2}');
    """

    return run_select_query(query)

compare_stock_trading_data = Query(
    variables=[Variables.STOCK_SYMBOL1, Variables.STOCK_SYMBOL2],
    fn=_compare_stock_trading_data
)


#
# -- compute correlation of two stock symbols
# select CORR_S(s1.Close, s2.Close) as Spearman_Correlation_Coeff from
# TradingData as s1 inner join TradingData as s2 on s1.Date = s2.Date
# where s1.stockID = (select ID from Stock where Symbol = '{stock_symbol1}') and
# s2.stockID = (select ID from Stock where Symbol = '{stock_symbol2}');
#
# def _compare_stock_correlation(stock_symbol1: str, stock_symbol2: str):
#     query = f"""
#     select CORR(s1.Close, s2.Close) as Spearman_Correlation_Coeff from
#     TradingData as s1 inner join TradingData as s2 on s1.Date = s2.Date
#     where s1.stockID = (select ID from Stock where Symbol = '{stock_symbol1}') and
#     s2.stockID = (select ID from Stock where Symbol = '{stock_symbol2}');
#     """
#
#     return run_select_query(query)
#
# compare_stock_correlation = Query(
#     variables=[Variables.STOCK_SYMBOL1, Variables.STOCK_SYMBOL2],
#     fn=_compare_stock_correlation
# )