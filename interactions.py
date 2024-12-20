from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

class Interactions:
    """Encapsulates an Amazon DynamoDB table of interactions.

    Example data structure for a movie record in this table:
        {
            "phone": "+13238745",
            "timestamp": "'12-19-24 20:43:36",
            "name": "Amanda",
            "received_message": "Hello World!",
            "sent_message": "And hello to you too"
        }
    """

    def __init__(self, dyn_resource, logger=None):
        """
        :param dyn_resource: A Boto3 DynamoDB resource.
        """
        self.dyn_resource = dyn_resource
        self.logger = logger
        # The table variable is set during the scenario in the call to
        # 'exists' if the table exists. Otherwise, it is set by 'create_table'.
        self.table = None


    def exists(self, table_name):
        """
        Determines whether a table exists. As a side effect, stores the table in
        a member variable.

        :param table_name: The name of the table to check.
        :return: True when the table exists; otherwise, False.
        """
        try:
            table = self.dyn_resource.Table(table_name)
            table.load()
            exists = True
        # except ClientError as err:
        #     if err.response["Error"]["Code"] == "ResourceNotFoundException":
        #         exists = False
        #     else:
        #         self.logger.error(
        #             "Couldn't check for existence of %s. Here's why: %s: %s",
        #             table_name,
        #             err.response["Error"]["Code"],
        #             err.response["Error"]["Message"],
        #         )
        #         raise
        except Exception as e:
            self.logger.error(e)
            raise e
        else:
            self.table = table
        return exists


    def create_table(self, table_name):
        """
        Creates an Amazon DynamoDB table that can be used to store interaction data.
        The table uses the phone the partition key and the
        timestamp as the sort key.

        :param table_name: The name of the table to create.
        :return: The newly created table.
        """
        try:
            self.table = self.dyn_resource.create_table(
                TableName=table_name,
                KeySchema=[
                    {"AttributeName": "phone", "KeyType": "HASH"},  # Partition key
                    {"AttributeName": "timestamp", "KeyType": "RANGE"},  # Sort key
                ],
                AttributeDefinitions=[
                    {"AttributeName": "phone", "AttributeType": "S"},
                    {"AttributeName": "timestamp", "AttributeType": "S"},
                ],
                ProvisionedThroughput={
                    "ReadCapacityUnits": 10,
                    "WriteCapacityUnits": 10,
                },
            )
            self.table.wait_until_exists()
        except ClientError as err:
            self.logger.error(
                "Couldn't create table %s. Here's why: %s: %s",
                table_name,
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            raise
        else:
            return self.table


    def list_tables(self):
        """
        Lists the Amazon DynamoDB tables for the current account.

        :return: The list of tables.
        """
        try:
            tables = []
            for table in self.dyn_resource.tables.all():
                print(table.name)
                tables.append(table)
        except ClientError as err:
            self.logger.error(
                "Couldn't list tables. Here's why: %s: %s",
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            raise
        else:
            return tables


    def add_interaction(self, phone, timestamp, name, received_message, sent_message):
        """
        Adds an interaction to the table.

        :param phone: The user's phone number
        :param timestamp: Timestamp when the user's message was received by the server
        :param name: The user's name
        :param received_message: Content of the received message
        :param sent_message: Content of the message server send back to user
        """
        try:
            self.table.put_item(
                Item={
                    "phone": phone,
                    "timestamp": timestamp,
                    "name": name,
                    "received_message": received_message,
                    "sent_message": sent_message
                }
            )
        except ClientError as err:
            self.logger.error(
                "Couldn't add interaction phone %s, timestamp %s to table %s. Here's why: %s: %s",
                phone,
                timestamp,
                self.table.name,
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            raise


    def query_interactions(self, phone):
        """
        Queries for interactions with the specified phone.

        :param phone: The phone to query.
        :return: The list of interactions with the specified phone.
        """
        try:
            response = self.table.query(KeyConditionExpression=Key("phone").eq(phone))
        except ClientError as err:
            self.logger.error(
                "Couldn't query for interactions with phone %s. Here's why: %s: %s",
                phone,
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            raise
        else:
            return response["Items"]


    # def delete_interactions(self, title, year):
    # TO BE DONE
    #     """
    #     Deletes a movie from the table.

    #     :param title: The title of the movie to delete.
    #     :param year: The release year of the movie to delete.
    #     """
    #     try:
    #         self.table.delete_item(Key={"year": year, "title": title})
    #     except ClientError as err:
    #         self.logger.error(
    #             "Couldn't delete movie %s. Here's why: %s: %s",
    #             title,
    #             err.response["Error"]["Code"],
    #             err.response["Error"]["Message"],
    #         )
    #         raise


    def delete_table(self):
        """
        Deletes the table.
        """
        try:
            self.table.delete()
            self.table = None
        except ClientError as err:
            self.logger.error(
                "Couldn't delete table. Here's why: %s: %s",
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            raise




