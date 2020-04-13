import os
import sys


sys.path.insert(0, '../..')

from monarch import config
from monarch.utils.tools import gen_random_key
from monarch.app import create_app
from monarch.models.menu import Menu
from monarch.models.permission import AppPermission
from monarch.models.oauth2 import OAuthApp


def main():
    default_app = OAuthApp.get_default()
    if not default_app:
        default_app = OAuthApp.create(
            client_id=gen_random_key(),
            client_secret=gen_random_key(),
            status=OAuthApp.STATUS_ON,
            name="智能客服平台",
            description="智能客服平台",
            homepage=config.SSO_URL,
            redirect_url=config.SSO_URL,
            white_list=True,
            is_default=True
        )
    all_menu = Menu.all()
    for menu in all_menu:
        AppPermission.create(
            app_id=default_app.id,
            name=menu.name,
            route_name="/",
            parent_id=menu.parent_id,
            permission_id=menu.id,
            remark="/",
        )


if __name__ == '__main__':
    app = create_app(os.getenv('BOILERPLATE_ENV') or 'dev')
    app.app_context().push()
    main()
