from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import Q

from applications.security.models import User
from applications.security.components.mixin_crud import CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin


class UserListView(PermissionMixin, ListViewMixin, ListView):
    template_name = 'security/user/list.html'
    model = User
    context_object_name = 'users'
    permission_required = 'view_user'

    def get_queryset(self):
        q1 = self.request.GET.get('q')
        if q1 is not None:
            self.query.add(Q(username__icontains=q1), Q.OR)
            self.query.add(Q(first_name__icontains=q1), Q.OR)
            self.query.add(Q(last_name__icontains=q1), Q.OR)
            self.query.add(Q(email__icontains=q1), Q.OR)
            self.query.add(Q(dni__icontains=q1), Q.OR)
        return self.model.objects.filter(self.query)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('security:user_create')
        return context


class UserCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = User
    template_name = 'security/user/form.html'
    fields = ['username', 'first_name', 'last_name', 'email', 'dni', 'direction', 
              'phone', 'image', 'groups', 'is_active', 'is_staff']
    success_url = reverse_lazy('security:user_list')
    permission_required = 'add_user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Grabar Usuario'
        context['back_url'] = self.success_url
        return context


class UserUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = User
    template_name = 'security/user/form.html'
    fields = ['username', 'first_name', 'last_name', 'email', 'dni', 'direction', 
              'phone', 'image', 'groups', 'is_active', 'is_staff']
    success_url = reverse_lazy('security:user_list')
    permission_required = 'change_user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Actualizar Usuario'
        context['back_url'] = self.success_url
        return context


class UserDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = User
    template_name = 'security/user/delete.html'
    success_url = reverse_lazy('security:user_list')
    permission_required = 'delete_user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Eliminar Usuario'
        context['description'] = f"¿Desea eliminar el usuario: {self.object.get_full_name}?"
        context['back_url'] = self.success_url
        return context
