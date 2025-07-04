from datetime import datetime
from django.contrib.auth.models import Group
from django.http import HttpRequest
from applications.security.models import GroupModulePermission, User

class MenuModule:
    def __init__(self, request: HttpRequest):
        self._request = request
        self._path = self._request.path

    def fill(self, data):
        data['user'] = self._request.user
        data['date_time'] = datetime.now()
        data['date_date'] = datetime.now().date()
        if self._request.user.is_authenticated and self._request.method == 'GET':
            data['group_list'] = self._request.user.groups.all().order_by('id')
            if 'group_id' not in self._request.session and data['group_list'].exists():
                self._request.session['group_id'] = data['group_list'].first().id
            if self._request.session.get('group_id'):
                group_id = self._request.GET.get('gpid', None)
                if group_id is not None:
                    self._request.session['group_id'] = data['group_list'].get(id=group_id).id
                group = Group.objects.get(id=self._request.session['group_id'])
                data['group'] = group
                data['menu_list'] = self.__get_menu_list(data["user"], group)

    def __get_menu_list(self, user: User, group: Group):
        group_module_permission_list = GroupModulePermission.objects.get_group_module_permission_active_list(group.id).order_by('module__menu__order', 'module__order')
        menu_ids = set()
        menu_list = []
        for permission in group_module_permission_list:
            menu = permission.module.menu
            if menu.id not in menu_ids:
                menu_ids.add(menu.id)
                menu_list.append(self._get_data_menu_list(permission, group_module_permission_list))
        return menu_list

    def _get_data_menu_list(self, group_module_permission: GroupModulePermission, group_module_permission_list):
        group_module_permissions = group_module_permission_list.filter(module__menu_id=group_module_permission.module.menu_id)
        return {
            'menu': group_module_permission.module.menu,
            'group_module_permission_list': group_module_permissions,
        }