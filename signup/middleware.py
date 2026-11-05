import ipaddress

from django.conf import settings
from django.http import Http404
from django.urls import NoReverseMatch, reverse


def _parse_networks(values):
    return [ipaddress.ip_network(value, strict=False) for value in values]


def _parse_ip(value):
    try:
        return ipaddress.ip_address(value.strip())
    except (AttributeError, ValueError):
        return None


class AdminIPRestrictionMiddleware:
    """
    Only allow requests to the Django admin from the networks listed in
    settings.ADMIN_ALLOWED_NETWORKS. Everyone else gets a 404.

    An empty ADMIN_ALLOWED_NETWORKS disables the restriction (e.g. for local
    development).

    The X-Forwarded-For header is only used when the request comes from an
    address in settings.ADMIN_TRUSTED_PROXIES, and then only its last entry
    (the address the proxy itself saw), so clients cannot spoof it.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.allowed_networks = _parse_networks(getattr(settings, 'ADMIN_ALLOWED_NETWORKS', []))
        self.trusted_proxies = _parse_networks(getattr(settings, 'ADMIN_TRUSTED_PROXIES', []))
        self._admin_prefix = None

    def __call__(self, request):
        if self.allowed_networks and request.path.startswith(self.admin_prefix):
            client_ip = self.get_client_ip(request)
            if client_ip is None or not any(client_ip in network for network in self.allowed_networks):
                raise Http404()
        return self.get_response(request)

    @property
    def admin_prefix(self):
        if self._admin_prefix is None:
            try:
                self._admin_prefix = reverse('admin:index')
            except NoReverseMatch:
                self._admin_prefix = '/admin/'
        return self._admin_prefix

    def get_client_ip(self, request):
        remote_ip = _parse_ip(request.META.get('REMOTE_ADDR'))
        if remote_ip is None:
            return None

        if any(remote_ip in network for network in self.trusted_proxies):
            forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR', '')
            if forwarded_for:
                return _parse_ip(forwarded_for.split(',')[-1])

        return remote_ip
