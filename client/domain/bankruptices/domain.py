from client.common.util import Domain, Option
from client.domain.bankruptices.queries import get_all_bankruptcy, insert_bankruptcy

bankruptcies = Domain(
    domain_name="Bankruptcies",
    options=[
        Option(id="Get All Bankruptcies", query=get_all_bankruptcy),
        Option(id="Create Bankruptcy", query=insert_bankruptcy),
    ]
)