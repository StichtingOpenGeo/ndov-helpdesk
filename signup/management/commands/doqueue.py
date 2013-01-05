#!/usr/bin/python
import tempfile, subprocess, os, glob

from django.core.management.base import BaseCommand
from django.core.mail import EmailMessage 

from signup.models import SignupQueue


class Command(BaseCommand):
    def __init__(self):
        BaseCommand.__init__(self)

    help = 'Process applications and send them a customized contract.'

    def handle(self, *args, **options):
        send_emails()


def send_emails():
    for request in SignupQueue.objects.filter(status=1):
        success, pdf = make_pdf(request.name, request.position, request.city, request.organization)
        if success:
            print "We created %s" % pdf
            send_created_contract(request.email, pdf)
            request.status = 2
            request.save()
            cleanup_tmp(pdf)


def send_created_contract(email, filename):
    email = EmailMessage("Your contract", "Attached is the file, please return.", 'noreply@opengeo.nl', [email])
    with open(filename) as f:
        email.attach('overeenkomst.pdf', f.read(), 'application/pdf')
        email.send()        
        
def make_pdf(name, position, city, organization=None):  
    ''' Write a LaTex file from our template '''
    # Write our prefix for the template
    templatestring = u"\\newcommand{\\tekenbevoegd}{%s}" % tex_clean(name)
    templatestring += u"\\newcommand{\\functie}{%s}" % tex_clean(position)
    templatestring += u"\\newcommand{\\vestigingsplaats}{%s}" % tex_clean(city)
    if organization is not None and organization != "":
        templatestring += "\\newcommand{\\onderneming}{%s}" % tex_clean(organization)
    
    # Read the rest of the template in
    templatestring += open('signup/management/commands/templates/overeenkomst-template.tex', 'r').read().decode('utf8')
    
    # Write out to a temporary file
    file = tempfile.NamedTemporaryFile(mode='w', prefix='ndov_signup-', suffix='.tex', delete=False)
    file.write(templatestring.encode('utf-8'))
    file.close()
    
    # Latex the temporary file to create a pdf
    print "Generated template at %s" % file.name
    try:
        with open(os.devnull, "w") as f: # We don't care so much about the output itself
            retcode = subprocess.call(["pdflatex", '--output-directory=%s' % os.path.dirname(file.name), file.name], stdout=f)
        if retcode < 0:
            cleanup_tmp(file.name)
            return (False, None)
        else:
            # We were successfull, return the name of the pdf
            return (True, "%s.pdf" % os.path.splitext(file.name)[0])
    except OSError as e:
        cleanup_tmp(file.name)
        return (False, None) # Log this error though!
    
def cleanup_tmp(name):
    ''' Cleanup all the files we created in the tmp directory '''
    for f in glob.glob("%s.*" % os.path.splitext(name)[0]):
        os.remove(f)
 
def tex_clean(string):
    ''' Remove anything that could be read by LaTex '''
    return string.strip('\@{}')

if __name__ == '__main__':
    send_emails()

