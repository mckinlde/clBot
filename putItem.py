class listings:
    """Encapsulates an Amazon DynamoDB table of listing data.

    Example data structure for a listing record in this table:
        {
            "url": "https://seattle.craigslist.org/see/cto/d/seattle-2021-ford-transit-connect/7781874621.html",
            "area": "seattle",
            "info": {
                "directors": ["Sam Raimi"],
                "release_date": "1999-09-15T00:00:00Z",
                "rating": 6.3,
                "plot": "A washed up pitcher flashes through his career.",
                "rank": 4987,
                "running_time_secs": 8220,
                "actors": [
                    "Kevin Costner",
                    "Kelly Preston",
                    "John C. Reilly"
                ]
            }
        }
    """

    def __init__(self, dyn_resource):
        """
        :param dyn_resource: A Boto3 DynamoDB resource.
        """
        self.dyn_resource = dyn_resource
        # The table variable is set during the scenario in the call to
        # 'exists' if the table exists. Otherwise, it is set by 'create_table'.
        self.table = None


    def add_listing(self, url, area, plot, rating):
        """
        Adds a listing to the table.

        :param url: The url of the listing.
        :param area: The release year of the listing.
        :param plot: The plot summary of the listing.
        :param rating: The quality rating of the listing.
        """
        try:
            self.table.put_item(
                Item={
                    "url": url,
                    "area": area,
                    "info": {"plot": plot, "rating": Decimal(str(rating))},
                }
            )
        except ClientError as err:
            logger.error(
                "Couldn't add listing %s to table %s. Here's why: %s: %s",
                title,
                self.table.name,
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            raise


aws dynamodb put-item \
    --table-name cars  \
    --item \
        '{"Artist": {"S": "No One You Know"}, "SongTitle": {"S": "Call Me Today"}, "AlbumTitle": {"S": "Somewhat Famous"}, "Awards": {"N": "1"}}'
