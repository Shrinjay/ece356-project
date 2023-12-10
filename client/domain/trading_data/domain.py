from client.common.util import Domain, Option
from client.domain.trading_data.queries import get_trading_data_for_stock, compare_stock_trading_data

trading_data = Domain(
                domain_name="Trading Data",
                options=[
                    Option(id="Get Trading Data for Stock", query=get_trading_data_for_stock),
                    Option(id="Compare Trading Data for 2 Stocks", query=compare_stock_trading_data),
                    # Option(id="Get Correlation for 2 Stocks", query=compare_stock_correlation)
                ]
            )