# coding=utf-8
from models import Configuracao, CustomUser
from django.contrib import admin

class ConfiguracaoAdmin(admin.ModelAdmin):

    list_display = ['nome', 'celular',]

    def has_add_permission(self, request): return False
    def has_delete_permission(self, request, obj=None): return False

    def get_actions(self, request):
        actions = super(ConfiguracaoAdmin, self).get_actions(request)
        if actions.get('delete_selected'): del actions['delete_selected']

        return actions

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name']

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Configuracao, ConfiguracaoAdmin)