import os
from collections.abc import Iterable

import boto3
import pytest
from boto3.resources.base import ServiceResource
from moto import mock_aws


@pytest.fixture()
def aws_credentials() -> None:
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "eu-central-1"


@pytest.fixture
def dynamodb_resource(aws_credentials: None) -> Iterable[ServiceResource]:
    with mock_aws():
        yield boto3.resource("dynamodb", region_name="eu-central-1")


@pytest.fixture
def dynamodb_table(dynamodb_resource: ServiceResource) -> ServiceResource:
    table_name = "test_db"
    table = dynamodb_resource.create_table(
        TableName=table_name,
        KeySchema=[
            {"AttributeName": "UserId", "KeyType": "HASH"},
            {"AttributeName": "Date", "KeyType": "RANGE"},
        ],
        AttributeDefinitions=[
            {"AttributeName": "UserId", "AttributeType": "S"},
            {"AttributeName": "Date", "AttributeType": "S"},
        ],
        ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
    )
    table.wait_until_exists()
    return table
