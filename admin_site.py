# coding: utf-8

from django.contrib.admin import AdminSite
from django.contrib.auth.admin import GroupAdmin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.core.urlresolvers import NoReverseMatch
from django.core.urlresolvers import reverse
from django.template.response import TemplateResponse
from django.utils.text import capfirst
from django.utils.translation import ugettext as _
from django.views.decorators.cache import never_cache


class NativeAdminSite(AdminSite):
    index_template = 'native_admin/index.html'
    auth_board_bottom = True

    boards = []
    auth_board = [
        (_(u'Authentication'), [
            (Group, GroupAdmin),
            (User, UserAdmin),
        ]),
    ]

    def __init__(self, *args, **kwargs):
        super(NativeAdminSite, self).__init__(*args, **kwargs)

        if self.auth_board_bottom:
            self.boards += self.auth_board

        if self.boards:
            for board_label, board_list in self.boards:
                for args_tuple in board_list:
                    self.register(*args_tuple)

    def get_boards_list(self, request):
        boards_list = []

        for board_label, board_list in self.boards:
            output_list = []

            for model_tuple in board_list:
                model = model_tuple[0]
                model_admin = self._registry[model]
                app_label = model._meta.app_label
                perms = model_admin.get_model_perms(request)

                # Check whether user has any perm for this module.
                # If so, add the module to the model_list.
                if True not in perms.values():
                    continue

                info = (app_label, model._meta.model_name)
                model_dict = {
                    'name': capfirst(model._meta.verbose_name_plural),
                    'object_name': model._meta.object_name,
                    'perms': perms,
                }

                if perms.get('change'):
                    try:
                        model_dict['admin_url'] = reverse(
                            'admin:%s_%s_changelist' % info, current_app=self.name)
                    except NoReverseMatch:
                        pass

                if perms.get('add'):
                    try:
                        model_dict['add_url'] = reverse(
                            'admin:%s_%s_add' % info, current_app=self.name)
                    except NoReverseMatch:
                        pass

                output_list.append(model_dict)

            if output_list:
                board_item = (board_label, output_list)
                boards_list.append(board_item)

        return boards_list

    @never_cache
    def index(self, request, extra_context=None):
        app_list = self.get_app_list(request)

        context = dict(
            self.each_context(request),
            title=self.index_title,
            boards_list=self.get_boards_list(request)
        )
        context.update(extra_context or {})

        request.current_app = self.name

        return TemplateResponse(request, self.index_template or
                                'admin/index.html', context)
