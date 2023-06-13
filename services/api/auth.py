import boto3


class UserManager:
    def __init__(self, client_id, user_pool_id):
        self.client_id = client_id
        self.user_pool_id = user_pool_id

    def sign_up(
        self,
        username,
        password,
        email,
        given_name,
        family_name,
    ):
        cognito_client = boto3.resource("cognito-idp")
        cognito_client.sign_up(
            ClientId=self.client_id,
            Username=username,
            Password=password,
            UserAttributes=[
                {"Name": "email", "Value": email},
                {"Name": "given_name", "Value": given_name},
                {"Name": "family_name", "Value": family_name},
            ],
        )

    """
    def authenticate(self, username, password):
        cognito_client = boto3.resources("cognito-idp")
        access_token = cognito_client.admin_initiate_auth
    """
