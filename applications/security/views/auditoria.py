from django.urls import reverse_lazy
from django.db.models import Q
from django.views.generic import ListView
from applications.security.components.mixin_crud import ListViewMixin, PermissionMixin
from applications.security.models import AuditUser


class AuditUserListView(PermissionMixin, ListViewMixin, ListView):
    template_name = 'security/auditoria/list.html'
    model = AuditUser
    context_object_name = 'audits'
    permission_required = 'view_audituser'

    def get_queryset(self):
        q1 = self.request.GET.get('q')
        if q1 is not None:
            self.query.add(Q(usuario__username__icontains=q1), Q.OR)
            self.query.add(Q(tabla__icontains=q1), Q.OR)
            self.query.add(Q(accion__icontains=q1), Q.OR)
            self.query.add(Q(estacion__icontains=q1), Q.OR)
        return self.model.objects.filter(self.query).select_related('usuario').order_by('-fecha', '-hora')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Auditoría de Usuarios'
        context['title1'] = 'Auditoría'
        return context
    