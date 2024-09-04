import boto3
from boto3.dynamodb.conditions import Key

# Initialize a session using Amazon DynamoDB
session = boto3.Session(region_name='us-west-2')  # Replace with your region
dynamodb = session.resource('dynamodb')

# Select your DynamoDB table
table = dynamodb.Table('cars')  # Replace with your table name

# Example of inserting an item
table.put_item(
    Item={
        'url': 'example',  # Replace with your primary key
        'Attribute1': 'value1',
        'Attribute2': 'value2'
    }
)

# Example of querying items
response = table.query(
    KeyConditionExpression=Key('url').eq('example')  # Replace with your key condition
)

items = response['Items']
for item in items:
    print(item)
