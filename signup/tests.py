from django.http import Http404, HttpResponse
from django.test import RequestFactory, SimpleTestCase, override_settings

from signup.management.commands.doqueue import tex_clean
from signup.middleware import AdminIPRestrictionMiddleware

__author__ = 'joelthuis'


class DoQueueTestCase(SimpleTestCase):
    def test_cleanstring(self):
        self.assertEqual(tex_clean('%Test'), 'Test')
        self.assertEqual(tex_clean('%Test@'), 'Test')
        self.assertEqual(tex_clean('%{Test}@'), 'Test')
        self.assertEqual(tex_clean('Test B.V.'), 'Test B.V.')
        self.assertEqual(tex_clean('Open-Geo'), 'Open-Geo')
        self.assertEqual(tex_clean('Jaap `~aap'), 'Jaap aap')


@override_settings(
    ADMIN_ALLOWED_NETWORKS=['10.9.0.0/24'],
    ADMIN_TRUSTED_PROXIES=['127.0.0.1/32'],
)
class AdminIPRestrictionMiddlewareTestCase(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def call(self, path, remote_addr, forwarded_for=None):
        middleware = AdminIPRestrictionMiddleware(lambda request: HttpResponse('ok'))
        extra = {'REMOTE_ADDR': remote_addr}
        if forwarded_for is not None:
            extra['HTTP_X_FORWARDED_FOR'] = forwarded_for
        return middleware(self.factory.get(path, **extra))

    def test_allows_admin_from_allowed_range(self):
        self.assertEqual(self.call('/admin/', '10.9.0.42').status_code, 200)
        self.assertEqual(self.call('/admin/signup/', '10.9.0.255').status_code, 200)

    def test_blocks_admin_from_outside_range(self):
        with self.assertRaises(Http404):
            self.call('/admin/', '10.9.1.1')
        with self.assertRaises(Http404):
            self.call('/admin/login/', '203.0.113.5')

    def test_other_paths_are_not_restricted(self):
        self.assertEqual(self.call('/aanmelden/', '203.0.113.5').status_code, 200)

    def test_uses_forwarded_for_from_trusted_proxy(self):
        self.assertEqual(self.call('/admin/', '127.0.0.1', '10.9.0.7').status_code, 200)
        with self.assertRaises(Http404):
            self.call('/admin/', '127.0.0.1', '203.0.113.5')

    def test_only_trusts_last_forwarded_for_entry(self):
        # A client can prepend anything; only the entry added by the proxy counts.
        with self.assertRaises(Http404):
            self.call('/admin/', '127.0.0.1', '10.9.0.7, 203.0.113.5')

    def test_ignores_forwarded_for_from_untrusted_source(self):
        with self.assertRaises(Http404):
            self.call('/admin/', '203.0.113.5', '10.9.0.7')

    def test_trusted_proxy_without_header_is_blocked(self):
        with self.assertRaises(Http404):
            self.call('/admin/', '127.0.0.1')

    def test_garbage_forwarded_for_is_blocked(self):
        with self.assertRaises(Http404):
            self.call('/admin/', '127.0.0.1', 'not-an-ip')

    @override_settings(ADMIN_ALLOWED_NETWORKS=[])
    def test_empty_allowlist_disables_restriction(self):
        self.assertEqual(self.call('/admin/', '203.0.113.5').status_code, 200)
