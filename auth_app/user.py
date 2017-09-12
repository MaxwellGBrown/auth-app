import boto3

from auth_app.util import scoped


class CognitoIdpClientFactory(object):
    """ A client-factory for AWS cognito_idp """

    def __init__(self, region_name=None):
        self.region_name = region_name

    def __call__(self):
        session = boto3.session.Session(region_name=self.region_name)
        return session.client('cognito-idp')


""" A "scoped_session" for cognito_idp """
cognito_idp = scoped(CognitoIdpClientFactory())


def configure_cognito_idp(**kwargs):
    """ Update the scoped `cognito_idp` factory to use **kwargs """
    cognito_idp.factory = CognitoIdpClientFactory(**kwargs)


class UserManager(object):

    # TODO Either config-ify this, or make a page that lists user pools too
    #      I guess I need more context into what exactly a user pool is
    UserPoolId = 'us-east-1_VauWvncW9'

    @classmethod
    def list_users(cls):
        # TODO Paginate
        response = cognito_idp.list_users(UserPoolId=cls.UserPoolId)

        user_list = []
        for user_dict in response['Users']:
            user_list.append(User(**user_dict))

        return user_list

    @classmethod
    def create_user(cls, username):
        """
        Create a new user in a user_pool.

        Since we're useing cognito-idp's `admin_create_user` we can only set a
        temporary password.
        """
        response = cognito_idp.admin_create_user(
            UserPoolId=cls.UserPoolId,
            Username=username
        )

        new_user = User(**response['User'])
        return new_user


class User(object):
    """ A python class that represents one aws cognito-idp User """

    user_type = 'basic'  # TODO
    token = None  # TODO

    def __init__(self, **raw):
        """ Initializes self.raw; everything else is a derived property """
        self.attributes = {d['Name']: d['Value'] for d in raw['Attributes']}

    @property
    def email(self):
        return self.attributes['email']

    @property
    def user_id(self):
        return self.attributes['sub']  # I think?
