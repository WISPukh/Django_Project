from django.contrib.auth.mixins import UserPassesTestMixin


class CheckUserIsOwnerMixin(UserPassesTestMixin):
    def test_func(self):
        return self.kwargs.get('pk') == self.request.user.pk
