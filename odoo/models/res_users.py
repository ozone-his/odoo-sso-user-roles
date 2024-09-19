import logging

from jose import jwt

from odoo import api, models

_logger = logging.getLogger(__name__)


class CustomUser(models.Model):
    _inherit = "res.users"

    @api.model
    def auth_oauth(self, provider, params):
        credentials = super().auth_oauth(provider, params)
        claims = jwt.get_unverified_claims(params['access_token'])
        odoo_access = claims['resource_access'].get('odoo')
        if odoo_access and odoo_access.get('roles'):
            odoo_roles = odoo_access.get('roles')
            _logger.info('Odoo Roles %s', odoo_roles)
        else:
            _logger.info('No Odoo roles defined in Keycloak')

        return credentials
