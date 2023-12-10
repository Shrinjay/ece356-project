from client.common.util import Domain, Option
from client.domain.analyst_ratings.queries import get_ratings, get_ratings_by_rating, get_all_ratings_for_analyst, get_all_analysts, insert_rating, auth_manager

analyst_ratings = Domain(
                domain_name="Analyst Ratings",
                options=[
                    Option(id="Get Analysts", query=get_all_analysts),
                    Option(id="Get All Ratings for an Analyst", query=get_all_ratings_for_analyst),
                    Option(id="Get Analyst Ratings for a Stock", query=get_ratings),
                    Option(id="Get Analyst Ratings by Rating", query=get_ratings_by_rating),
                    Option(id="Add Rating", query=insert_rating),
                ]
            )