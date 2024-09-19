import logging

from jose import jwt

from odoo import api, models

_logger = logging.getLogger(__name__)


class CustomUser(models.Model):
    _inherit = "res.users"

    @api.model
    def auth_oauth(self, provider, params):
        credentials = super().auth_oauth(provider, params)
        _logger.info('Credentials %s', credentials)
        user = self.search([("login", "=", credentials[0]), ('oauth_access_token', '=', params['access_token'])])
        _logger.info('User %s', user)
        # user = self.search([("oauth_uid", "=", oauth_uid), ('oauth_provider_id', '=', provider)])
        claims = jwt.get_unverified_claims(params['access_token'])
        odoo_access = claims['resource_access'].get('odoo')
        if odoo_access and odoo_access.get('roles'):
            odoo_roles = odoo_access.get('roles')
            _logger.info('Odoo Roles %s', odoo_roles)
            group_ids = []
            for r in odoo_roles:
                group_id = self.env["res.groups"].search([("name", "=", r)])
                if group_id:
                    group_ids.append(group_id)
            _logger.info('Group Ids %s', group_ids)
            user.write({'groups_id': [(6, 0, group_ids)]})
        else:
            _logger.info('No Odoo roles defined in Keycloak')

        return credentials
