from common.util import Client

from domain.financial_data.domain import financial_data
from domain.trading_data.domain import trading_data
from domain.analyst_ratings.domain import analyst_ratings, auth_manager
from domain.ipo.domain import ipo
from domain.bankruptices.domain import bankruptcies

# Option
# ID
# Variables
# Function



def main():
    client = Client(
        domains=[trading_data, financial_data, analyst_ratings, ipo, bankruptcies]
    )

    auth_manager.authenticate()
    auth_manager.get_analyst_id()
    client.run()


if __name__ == '__main__':
    main()


