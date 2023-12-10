from client.common.util import run_insert_query, run_select_query
from client.common.util import Query, Variables
import datetime
import pandas as pd

def _get_ipo(stock_symbol: str):
    query = f"""
        select PricePerShare, NumShares from IPO
        where eventID IN (select ID from Event where stockID = (select ID from Stock where Symbol = '{stock_symbol}') and Type = 'IPO');
        """
    return run_select_query(query)


get_ipo = Query(variables=[Variables.STOCK_SYMBOL], fn=_get_ipo)


def _insert_ipo(stock_symbol: str, date: datetime.date, price_per_share: float, num_shares: int) -> pd.DataFrame:
    str_date = date.strftime("%Y-%m-%d")

    create_event_query = f"""
    INSERT INTO Event
    (stockID, `Date`, `Type`)
    VALUES((select ID from Stock where Symbol = '{stock_symbol}'), STR_TO_DATE('{str_date}', '%Y-%m-%d'), 'IPO');
    """
    event_id = run_insert_query(create_event_query)

    create_ipo_query = f"""
    INSERT INTO IPO
    (eventID, PricePerShare, NumShares)
    VALUES({event_id}, {price_per_share}, {num_shares});
    """
    ipo_id = run_insert_query(create_ipo_query)

    return get_ipo_by_id(ipo_id)

insert_ipo = Query(variables=[Variables.STOCK_SYMBOL, Variables.DATE, Variables.PRICE_PER_SHARE, Variables.NUM_SHARES], fn=_insert_ipo)


def get_ipo_by_id(id: int):
    query = f"""
    SELECT ID, eventID, PricePerShare, NumShares
    FROM IPO
    where id = {id};
    """

    return run_select_query(query)

# -- get all IPO data
# select Stock.Symbol, IPO.PricePerShare, IPO.NumShares, Event.Date
# from Stock inner join Event on Stock.ID = Event.stockID
# inner join IPO on IPO.eventID = Event.ID;


def _get_all_ipo():
    query = f"""       
    select Stock.Symbol, IPO.PricePerShare, IPO.NumShares, Event.Date
    from Stock inner join Event on Stock.ID = Event.stockID
    inner join IPO on IPO.eventID = Event.ID;
    """

    return run_select_query(query)


get_all_ipo = Query(variables=[], fn=_get_all_ipo)