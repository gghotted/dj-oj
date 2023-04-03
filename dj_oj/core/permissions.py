from braces.views import PermissionRequiredMixin as _PermissionRequiredMixin
from django.contrib import messages


class PermissionRequiredMixin(_PermissionRequiredMixin):

    def no_permissions_fail(self, request=None):
        messages.add_message(
            self.request,
            messages.ERROR,
            '접근 권한이 없습니다, 권한이 있는 계정으로 로그인해주세요',
        )
        return super().no_permissions_fail(request)
