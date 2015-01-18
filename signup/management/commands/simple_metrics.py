from django.core.management import BaseCommand, CommandError
from signup.models import SignupQueue

__author__ = 'joelthuis'


class Command(BaseCommand):
    """
    Following template at http://codeinthehole.com/writing/integrating-django-application-metrics-into-zabbix/
    """

    def handle(self, *args, **options):
        if not args:
            print self.print_usage()
            return
        method_name = 'fetch_%s' % args[0]
        if not hasattr(self, method_name):
            raise CommandError("No method found with name '%s'" % method_name)
        print getattr(self, method_name)(*args[1:])

    def print_usage(self):
        fetchers = [m for m in dir(self) if m.startswith('fetch')]
        descriptions = []
        for fetcher in fetchers:
            method = getattr(self, fetcher)
            docstring = method.__doc__.strip() if method.__doc__ else "<no description>"
            descriptions.append(" - %s : %s" % (
                '_'.join(fetcher.split("_")[1:]), docstring))
        return "Available fetchers:\n%s" % "\n".join(descriptions)

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