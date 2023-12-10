from client.common.util import run_insert_query, run_select_query
from client.common.util import Query, Variables
import datetime

def _get_all_bankruptcy():
    query = f"""
        select Stock.Symbol,Bankruptcy.FilingType, Event.Date
        from Event inner join Stock on Event.stockID = Stock.ID
        inner join Bankruptcy on Bankruptcy.eventID = Event.ID;
    """

    return run_select_query(query)


get_all_bankruptcy = Query(variables=[], fn=_get_all_bankruptcy)


def get_bankruptcy_by_id(id: int):
    query = f"""
    SELECT * FROM Bankruptcy where ID = id;
    """

    return run_select_query(query)


def _insert_bankruptcy(stock_symbol: str, date: datetime.date, filing_type: str):
    str_date = date.strftime("%Y-%m-%d")

    create_event_query = f"""
    INSERT INTO Event
    (stockID, `Date`, `Type`)
    VALUES((select ID from Stock where Symbol = '{stock_symbol}'), STR_TO_DATE('{str_date}', '%Y-%m-%d'), 'IPO');
    """
    event_id = run_insert_query(create_event_query)

    create_bankruptcy_query = f"""
    INSERT INTO Bankruptcy
    (eventID, FilingType)
    VALUES({event_id}, '{filing_type}');
    """
    bankruptcy_id = run_insert_query(create_bankruptcy_query)

    return get_bankruptcy_by_id(bankruptcy_id)

insert_bankruptcy = Query(
    variables=[Variables.STOCK_SYMBOL, Variables.DATE, Variables.FILING_TYPE],
    fn=_insert_bankruptcy
)
