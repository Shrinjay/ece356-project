from client.common.util import Domain, Option
from client.domain.ipo.queries import get_ipo, get_all_ipo, insert_ipo

ipo = Domain(
        domain_name="IPO",
        options=[
            Option(id="Get IPO for stock", query=get_ipo),
            Option(id="Get All IPOs", query=get_all_ipo),
            Option(id="Create IPO", query=insert_ipo)
        ]
    )