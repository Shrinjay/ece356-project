from client.common.util import run_insert_query, run_select_query
from client.common.util import Query, Variables, AnalystRating
from client.common.auth import auth_manager
import datetime

def _get_ratings(stock_symbol: str):
    query = f"""
    select Date, Rating, InternalUser.username as Name, Analyst.id as AnalystID, Firm.Name as FirmName, TargetPrice from AnalystRating
    inner join Analyst on Analyst.ID = AnalystRating.ID
    inner join InternalUser on InternalUser.ID = Analyst.userID
    inner join Firm on Firm.ID = Analyst.firmID
    where stockID = (select ID from Stock where Symbol = '{stock_symbol}');
    """

    return run_select_query(query)


get_ratings = Query(
    variables=[Variables.STOCK_SYMBOL],
    fn=_get_ratings
)


# -- given a stock symbol find all analyst ratings for that particular stock symbol with a particular rating
# select Date, Rating, TargetPrice from AnalystRating
# where stockID = (select ID from Stock where Symbol = '{stock_symbol}')
# and Rating = '{rating}';
def _get_ratings_by_rating(stock_symbol: str, rating: AnalystRating):
    query = f"""
    select Date, Rating, InternalUser.username as Name, Analyst.id as AnalystID, Firm.Name as FirmName, TargetPrice from AnalystRating
    inner join Analyst on Analyst.ID = AnalystRating.ID
    inner join InternalUser on InternalUser.ID = Analyst.userID
    inner join Firm on Firm.ID = Analyst.firmID
    where stockID = (select ID from Stock where Symbol = '{stock_symbol}')
    and Rating = '{rating}';
    """

    return run_select_query(query)


get_ratings_by_rating = Query(
    variables=[Variables.STOCK_SYMBOL, Variables.RATING],
    fn=_get_ratings_by_rating
)


def get_rating_by_id(id: int):
    query = f"""
    SELECT * FROM AnalystRating where ID = {id};
    """

    return run_select_query(query)


def _insert_rating(stock_symbol: str, rating: str, target_price: float):
    analyst_id = auth_manager.get_analyst_id()
    now = datetime.datetime.now()
    str_date = now.strftime("%Y-%m-%d")

    query = f"""
    INSERT INTO AnalystRating
    (stockID, analystID, `Date`, Rating, TargetPrice)
    VALUES((select ID from Stock where Symbol = '{stock_symbol}'), {analyst_id}, STR_TO_DATE('{str_date}', '%Y-%m-%d'), '{rating}', {target_price});
    """

    rating_id = run_insert_query(query)

    return get_rating_by_id(rating_id)

insert_rating = Query(
    variables=[Variables.STOCK_SYMBOL, Variables.RATING, Variables.TARGET_PRICE],
    fn=_insert_rating
)

def _get_all_analysts():
    query = f"""
        select Analyst.ID as AnalystID, Firm.Name as FirmName from Analyst
        inner join Firm on Firm.ID = Analyst.firmID
    """

    return run_select_query(query)

get_all_analysts = Query(
    variables=[],
    fn=_get_all_analysts
)


def _get_all_ratings_for_analyst(analyst_id: int):
    query = f"""
        select Stock.Symbol, AnalystRating.Date, AnalystRating.Rating, AnalystRating.TargetPrice
        from AnalystRating inner join Stock on AnalystRating.stockID = Stock.ID
        where analystID = '{analyst_id}';
    """

    return run_select_query(query)


get_all_ratings_for_analyst = Query(
    variables=[Variables.ANALYST],
    fn=_get_all_ratings_for_analyst
)