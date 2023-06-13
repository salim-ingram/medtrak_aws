import boto3


class UserManager:
    def __init__(self, user_pool, user_client):
        self.user_pool = user_pool
        self.user_client = user_client

    def sign_up(
        self,
        username,
        password,
        email,
        given_name,
        family_name,
    ):
        cognito_client = boto3.client("cognito-idp")
        cognito_client.sign_up(
            ClientId=self.user_client["UserPoolClient"]["ClientId"],
            Username=username,
            Password=password,
            UserAttributes=[
                {"Name": "email", "Value": email},
                {"Name": "given_name", "Value": given_name},
                {"Name": "family_name", "Value": family_name},
            ],
        )

    def get_user_admin(self, username):
        cognito_client = boto3.client("cognito-idp")
        user = cognito_client.admin_get_user(
            UserPoolId=self.user_pool["Id"],
            Username=username,
        )
        return user
