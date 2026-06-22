from django.shortcuts import redirect
from django.urls import reverse

class LoginRequiredMiddleware:
    """บังคับให้ผู้ใช้ล็อกอินก่อนเข้าใช้งาน"""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        allowed_paths = [
            reverse('login'),
            reverse('account_login'),
            reverse('account_signup'),
            reverse('password_reset'),
            reverse('password_reset_done'),
            reverse('password_reset_confirm', kwargs={'uidb64': 'uid', 'token': 'token'}),
            reverse('password_reset_complete'),
        ]

        if not request.user.is_authenticated:
            if not any(request.path.startswith(path) for path in allowed_paths) and not request.path.startswith('/admin/'):
                return redirect('login')

        return self.get_response(request)
