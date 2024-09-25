import contextlib
import logging

from jose import jwt
from odoo.addons.website.tools import MockRequest
from odoo.tools.misc import DotDict

from odoo.tests import common

CLIENT_ID = "auth_oidc-test"

logger = logging.getLogger(__name__)


@contextlib.contextmanager
def create_request(env, user_id):
    with MockRequest(env) as request:
        request.session = DotDict(uid=user_id)
        yield request


class TestOpenIDRoleAssignment(common.HttpCase):
    def setUp(self):
        super().setUp()
        # search our test provider and bind the demo user to it
        self.provider = self.env["auth.oauth.provider"].search(
            [("client_id", "=", CLIENT_ID)]
        )
        self.assertEqual(len(self.provider), 1)

    def _prepare_login_test_user(self, provider_id, token):
        user = self.env.ref("base.user_demo")
        user.write({
            "oauth_provider_id": provider_id.id,
            "oauth_uid": user.login,
            "oauth_access_token": token
        })
        return user

    def test_oidc_role_assignment(self):
        """Test that the roles in the provider are assigned to the user"""
        role_currencies = 'Extra Rights / Multi Currencies'
        role_companies = 'Extra Rights / Multi Companies'
        claims = {
            "resource_access": {
                "odoo": {
                    "roles": [
                        role_currencies,
                        role_companies
                    ]
                }
            }
        }
        token = jwt.encode(claims, 'test', algorithm='HS256')
        user = self._prepare_login_test_user(self.provider, token)
        group_id_1 = self.env["res.groups"].search([("full_name", "=", role_currencies)])
        group_id_2 = self.env["res.groups"].search([("full_name", "=", role_companies)])
        self.assertFalse(group_id_1 in user.groups_id)
        self.assertFalse(group_id_2 in user.groups_id)
        credentials = ('', user.login, '')
        params = {'access_token': token}
        with create_request(self.env, user.id):
            user.assign_roles(credentials, params)
            self.assertTrue(group_id_1 in user.groups_id)
            self.assertTrue(group_id_2 in user.groups_id)
