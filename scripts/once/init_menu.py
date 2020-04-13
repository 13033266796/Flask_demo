import os
import sys

sys.path.insert(0, '../..')

from monarch.app import create_app
from monarch.models.menu import Menu

MENU_DEFAULT_DATA = [
    {
        "name": "后台",
        "children": [
            {
                "children": [
                    {
                        "name": "所有用户",
                    },
                    {
                        "name": "角色设置",
                    }
                ],
                "name": "用户管理",
            },

            {
                "name": "企业设置",
            }
        ]
    }
]


def main():
    menu_data = MENU_DEFAULT_DATA
    for children_menu in menu_data:
        menu = Menu.get_by_name_and_parent_id(name=children_menu.get("name"), parent_id=0)
        if not menu:
            menu = Menu.create(name=children_menu.get("name"), parent_id=0)

        s_children_menu_data = children_menu.get("children", [])
        if s_children_menu_data:
            for s_children in s_children_menu_data:
                s_children_menu = Menu.get_by_name_and_parent_id(name=s_children.get("name"), parent_id=menu.id)
                if not s_children_menu:
                    s_children_menu = Menu.create(name=s_children.get("name"), parent_id=menu.id)

                t_children_menu_data = s_children.get("children", [])
                if t_children_menu_data:
                    for t_children in t_children_menu_data:
                        t_children_menu = Menu.get_by_name_and_parent_id(name=t_children.get("name"),
                                                                         parent_id=s_children_menu.id)
                        if not t_children_menu:
                            t_children_menu = Menu.create(name=t_children.get("name"), parent_id=s_children_menu.id)

                        f_children_menu_data = t_children.get("children", [])
                        if f_children_menu_data:
                            for f_children in f_children_menu_data:
                                f_children_menu = Menu.get_by_name_and_parent_id(name=f_children.get("name"),
                                                                                 parent_id=t_children_menu.id)
                                if not f_children_menu:
                                    Menu.create(name=f_children.get("name"), parent_id=t_children_menu.id)


if __name__ == '__main__':
    app = create_app(os.getenv('BOILERPLATE_ENV') or 'dev')
    app.app_context().push()
    main()
