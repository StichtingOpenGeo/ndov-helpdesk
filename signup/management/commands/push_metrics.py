import logging
import protobix
from django.core.management import BaseCommand
from signup.models import SignupQueue

logger = logging.getLogger('push_metrics')


class Command(BaseCommand):

    def handle(self, *args, **options):
        data = {
            'fr.ovapi.nl': {
                'ndovloket.aanmelding.verwerkt': 0,
                'ndovloket.aanmelding.ondertekend': 0,
                'ndovloket.aanmelding.fouten': 0,
                }
        }

        data['fr.ovapi.nl']['ndovloket.aanmelding.verwerkt'] = self.fetch_signups_processed()
        data['fr.ovapi.nl']['ndovloket.aanmelding.ondertekend'] = self.fetch_signups_open()
        data['fr.ovapi.nl']['ndovloket.aanmelding.fouten'] = self.fetch_signups_error()

        zbx_container = protobix.DataContainer("items", "localhost", 10051)
        zbx_container.add(data)

        ret = zbx_container.send(zbx_container)
        if not ret:
            print logger.error("Ooops. Something went wrong when sending data to Zabbix")
        else:
            print logger.debug("Everything is OK")

    def fetch_signups_open(self):
        """
        Number of signups that haven't been generated
        """
        return SignupQueue.objects.filter(status=1).count()

    def fetch_signups_processed(self):
        """
        Number of signups that have been processed
        """
        return SignupQueue.objects.filter(status=4).count()

    def fetch_signups_error(self):
        """
        Number of signups that have errors
        """
        return SignupQueue.objects.filter(status=5).count()