#!/usr/bin/python
import tempfile, subprocess, os, glob, re, logging
from datetime import datetime
import unidecode
from django.core.management.base import BaseCommand
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import get_template
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from signup.models import SignupQueue

logger = logging.getLogger('cli_actions')


class Command(BaseCommand):
    def __init__(self):
        BaseCommand.__init__(self)

    help = 'Process applications and send them a customized contract.'

    def handle(self, *args, **options):
        send_emails()


def send_emails():
    ''' For each application that doesn't have a contract mailed, create one '''
    logger.info("Running queue for %s signups" % (SignupQueue.objects.filter(status=1).count()))

    for request in SignupQueue.objects.filter(status=1):
        success, pdf = make_pdf(request.name, request.position, request.city, request.organization)
        if success:
            username, password = create_account(request.name, request.email)
            if username is not None:
                send_created_contract(request, username, password, pdf)
                print("We sent a contract (%s) to %s <%s>" % (pdf, request.name, request.email))
                logger.info("We sent a contract (%s) to %s" % (pdf, request.name))

                # Update the status once everything is ok
                request.status = 2
                request.save()
            else:
                logger.info("Setting status for %s to error (PDF: %s)" % (request.name, pdf))
                request.status = 5
                request.save()
                send_error(request)

            cleanup_tmp(pdf)  # Cleanup our mess
        else:
            logger.info("Something went wrong here :( (%s, %s)" % (success, pdf))
            request.status = 5
            request.save()
            send_error(request)


def send_created_contract(request, username, password, filename):
    # Determine name to use
    name = request.name
    if request.organization is not None and request.organization != "":
        name = request.organization

    # Setup email
    email_template = get_template('signup/nl/email_contract.txt')
    email_context = {'name': request.name, 'username': username, 'password': password}
    subject = _("NDOV overeenkomst voor %(name)s ") % {'name': name}
    email = EmailMessage(subject, email_template.render(email_context), getattr(settings, 'DEFAULT_FROM_EMAIL'),
                         [request.email])

    attachment_name = 'overeenkomst-%s-%s.pdf' % (unidecode.unidecode(name).lower().replace(' ', '_').replace('_', ''), datetime.now().strftime("%Y%m%d"))
    with open(filename, 'rb') as f:
        email.attach(attachment_name, f.read(), 'application/pdf')
    email.send()


def send_error(request):
    email_template = get_template('signup/nl/email_error.txt')
    email_context = {'name': request.name, 'organization': request.organization}
    subject = "[NDOV] Fout bij aanmaken overeenkomst"
    email = EmailMessage(subject, email_template.render(email_context),
                         getattr(settings, 'DEFAULT_FROM_EMAIL'), [getattr(settings, 'SIGNUP_ERROR_EMAIL')])
    email.send()


def create_account(name, email):
    """ Create a new account with a random password and make sure we have a unique username """
    password = User.objects.make_random_password()
    username = re.sub(r'[^\w]', '', unidecode.unidecode(name.lower()))  # Remove anything not a word character/letter
    logger.info("We're creating a user account <%s>" % (username))

    # Generate a unique username, append a number if we can't
    suffix_number = 1
    while User.objects.filter(username__exact=username).count() > 0:
        logger.debug("Username <%s> already exists, using suffix %s" % (username, suffix_number))
        # TODO this works till 10
        username = "%s%i" % (username[:-1] if suffix_number > 1 else username, suffix_number)
        suffix_number += 1

    try:
        User.objects.create_user(username, email, password)
        return username, password
    except:  # Database errors
        return None, None


def make_pdf(name, position, city, organization=None):
    """ Write a LaTex file from our template
    Write our prefix with variables for the template - NOTE: escaped slashes! """
    templatestring = u"\\newcommand{\\tekenbevoegd}{%s}" % tex_clean(name)
    templatestring += u"\\newcommand{\\functie}{%s}" % tex_clean(position)
    templatestring += u"\\newcommand{\\vestigingsplaats}{%s}" % tex_clean(city)
    if organization is not None and organization != "":
        templatestring += "\\newcommand{\\onderneming}{%s}" % tex_clean(organization)

    # Read the actual template
    templatestring += open('signup/management/commands/templates/overeenkomst-template.tex', 'r').read()

    # Write the complete template out to a temporary file
    file = tempfile.NamedTemporaryFile(mode='w', prefix='ndov_signup-', suffix='.tex', delete=False)
    file.write(templatestring)
    file.close()
    logger.debug("Wrote template tex out to %s" % file.name)

    # Latex the temporary file to create a pdf
    try:
        with open(os.devnull, "w") as f:  # We don't care so much about the output itself, write to /dev/null
            retcode = subprocess.call(["pdflatex", '--output-directory=%s' % os.path.dirname(file.name), file.name],
                                      stdout=f)
        if retcode < 0:
            logger.debug("Error creating pdf from latex, return code not positive")
            cleanup_tmp(file.name)
            return (False, None)
        else:
            # We were successful, return the name of the pdf
            filename = "%s.pdf" % os.path.splitext(file.name)[0]
            return True, filename
    except OSError as e:
        logger.debug("Error creating pdf from latex, removing latex: %s" % (e))
        cleanup_tmp(file.name)
        return False, None


def cleanup_tmp(name):
    """ Cleanup all the files we created in the tmp directory """
    for f in glob.glob("%s.*" % os.path.splitext(name)[0]):
        os.remove(f)


def tex_clean(string):
    """ Remove anything that could be read by LaTex as a command / variable """
    # return string.strip('\@{}%')
    return re.sub(r'[^\w .-]', '', string)


if __name__ == '__main__':
    send_emails()
