import boto3
import pytest
from auth import UserManager
from fastapi import status
from main import app
from moto import mock_cognitoidp
from starlette.testclient import TestClient


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
def user_pool():
    with mock_cognitoidp():
        client = boto3.client("cognito-idp")
        user_pool = client.create_user_pool(PoolName="TestUserPool")["UserPool"]

        yield user_pool


@pytest.fixture
def user_client(user_pool):
    client = boto3.client("cognito-idp")
    user_client = client.create_user_pool_client(
        UserPoolId=user_pool["Id"],
        ClientName="TestAppClient",
    )

    yield user_client


def test_thing(user_pool, user_client):
    user_client_id = user_client["UserPoolClient"]["ClientId"]
    user_pool_id = user_pool["Id"]
    print("user pool id", user_pool_id)
    print("user client id", user_client_id)


def test_user_sign_up(user_pool, user_client):
    client = boto3.client("cognito-idp")
    new_username = "random-username"
    user_manager = UserManager(user_pool=user_pool, user_client=user_client)
    new_user = user_manager.sign_up(
        username=new_username,
        password="TestPassword123!",
        email="user@example.com",
        given_name="FirstName",
        family_name="LastName",
    )
    client.admin_confirm_sign_up(
        UserPoolId=user_pool["Id"],
        Username=new_username,
    )

    print(new_user)
