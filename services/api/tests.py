import boto3
import pytest
from fastapi import status
from moto import mock_cognitoidp
from starlette.testclient import TestClient

from main import app
from models import User


@pytest.fixture
def client():
    return TestClient(app)


def test_health_check(client):
    """
    GIVEN
    WHEN health check endpoint is called with GET method
    THEN response with status 200 and body OK is returned
    """
    response = client.get("/api/health-check/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "OK"}


@pytest.fixture
def cognito_user_pool():
    with mock_cognitoidp():
        client = boto3.client("cognito-idp")
        user_pool = client.create_user_pool(PoolName="TestUserPool")["UserPool"]

        app_client = client.create_user_pool_client(
            UserPoolId=user_pool["Id"],
            ClientName="TestAppClient",
        )
