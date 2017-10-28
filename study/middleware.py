from django.http import HttpResponseRedirect

from django.urls import resolve, reverse


class AuthenticationMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        assert hasattr(request, 'user')

        r = resolve(request.path)

        if request.user.is_authenticated():
            if 'dashboard' not in r.namespaces and r.url_name != 'logout':
                return HttpResponseRedirect(reverse('study:dashboard:index'))
        else:
            if 'dashboard' in r.namespaces:
                return HttpResponseRedirect(reverse('study:login'))

        response = self.get_response(request)

        return response
