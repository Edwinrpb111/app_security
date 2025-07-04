from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q

from applications.security.components.mixin_crud import PermissionMixin
from applications.security.models import GroupModulePermission

class GroupModulePermissionListView(LoginRequiredMixin, PermissionMixin, ListView):
    model = GroupModulePermission
    template_name = 'security/group_module_permission/list.html'
    context_object_name = 'group_module_permissions'
    permission_required = 'security.view_groupmodulepermission'
    paginate_by = 20

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return self.model.objects.filter(
                Q(group__name__icontains=query) |
                Q(module__name__icontains=query)
            ).select_related('group', 'module')
        return self.model.objects.all().select_related('group', 'module')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('security:group_module_permission_create')
        return context

class GroupModulePermissionCreateView(LoginRequiredMixin, PermissionMixin, CreateView):
    model = GroupModulePermission
    template_name = 'security/group_module_permission/form.html'
    fields = ['group', 'module', 'permissions']
    success_url = reverse_lazy('security:group_module_permission_list')
    permission_required = 'security.add_groupmodulepermission'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Crear Permiso de Grupo-Módulo'
        context['back_url'] = reverse_lazy('security:group_module_permission_list')
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Permiso para "{self.object.group.name} - {self.object.module.name}" creado exitosamente.')
        return response

class GroupModulePermissionUpdateView(LoginRequiredMixin, PermissionMixin, UpdateView):
    model = GroupModulePermission
    template_name = 'security/group_module_permission/form.html'
    fields = ['group', 'module', 'permissions']
    success_url = reverse_lazy('security:group_module_permission_list')
    permission_required = 'security.change_groupmodulepermission'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Actualizar Permiso de Grupo-Módulo'
        context['back_url'] = reverse_lazy('security:group_module_permission_list')
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Permiso para "{self.object.group.name} - {self.object.module.name}" actualizado exitosamente.')
        return response

class GroupModulePermissionDeleteView(LoginRequiredMixin, PermissionMixin, DeleteView):
    model = GroupModulePermission
    template_name = 'security/group_module_permission/delete.html'
    success_url = reverse_lazy('security:group_module_permission_list')
    permission_required = 'security.delete_groupmodulepermission'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Eliminar Permiso de Grupo-Módulo'
        context['description'] = f'¿Está seguro de que desea eliminar el permiso de "{self.object.group.name}" para el módulo "{self.object.module.name}"?'
        context['back_url'] = reverse_lazy('security:group_module_permission_list')
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        messages.success(request, f'Permiso para "{self.object.group.name} - {self.object.module.name}" eliminado exitosamente.')
        return super().delete(request, *args, **kwargs)
