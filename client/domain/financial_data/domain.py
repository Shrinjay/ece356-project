from client.common.util import Domain, Option
from client.domain.financial_data.queries import get_financial_data, get_financial_data_for_stock

financial_data = Domain(
                domain_name="Financial Data",
                options=[
                    Option(id="Get Financial Data for Stock", query=get_financial_data_for_stock),
                    Option(id="Get Financial Data", query=get_financial_data)
                ]
            )