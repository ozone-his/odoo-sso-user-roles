{
    "name": "${project.name}",
    'version': '${odooVersion}.${addonVersion}',
    "license": "AGPL-3",
    "author": (
        "Mekom Solutions"
    ),
    "website": "https://github.com/ozone-his/ozone-auth-roles/odoo",
    "summary": "Assigns the roles defined in the authentication provider to a user as groups upon login",
    "depends": ["auth_oidc"],
    "data": [],
    "demo": [],
    "installable": True,
    "auto_install": True
}
