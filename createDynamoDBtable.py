# Python code to create a table to store Twitter hashtags in DynamoDB.

import boto3

dynamodb = boto3.resource('dynamodb')

table = dynamodb.create_table(
    TableName='hashtags',
    KeySchema=[
        {
            'AttributeName': 'hashtag',
            'KeyType': 'HASH'
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'hashtag',
            'AttributeType': 'S'
        }

    ],
    # Pricing determined by ProvisionedThroughput.
    ProvisionedThroughput={
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }
)

table.meta.client.get_waiter('table_exists').wait(TableName='hashtags')

# Print out some data about the table.
print(table.item_count)