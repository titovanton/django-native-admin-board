# -*- coding: utf-8 -*-

from django.contrib.admin import ModelAdmin as ModelAdminBase


class ModelAdmin(ModelAdminBase):
    change_list_template = 'native_admin/change_list.html'
    change_form_template = 'native_admin/change_form.html'
