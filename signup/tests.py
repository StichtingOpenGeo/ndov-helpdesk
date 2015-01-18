from django.utils.unittest.case import TestCase
from signup.management.commands.doqueue import tex_clean

__author__ = 'joelthuis'


class DoQueueTestCase(TestCase):
    def test_cleanstring(self):
        self.assertEqual(tex_clean('%Test'), 'Test')
        self.assertEqual(tex_clean('%Test@'), 'Test')
        self.assertEqual(tex_clean('%{Test}@'), 'Test')
        self.assertEqual(tex_clean('Test B.V.'), 'Test B.V.')
        self.assertEqual(tex_clean('Open-Geo'), 'Open-Geo')
        self.assertEqual(tex_clean('Jaap `~aap'), 'Jaap aap')
