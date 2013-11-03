# from os.path import basename
from wsgiref.util import FileWrapper
from os import environ
from subprocess import call as call_subprocess, list2cmdline
from tempfile import NamedTemporaryFile
# import hashlib

from django.http import HttpResponse
from django.template import RequestContext, Context
from django.template.loader import get_template
from django.utils import simplejson
# from django.core.servers.basehttp import FileWrapper

# from pywkher import generate_pdf
from Syllia.apps.syllabus.models import College, Department, Rubric, Syllabus


def return_a_pdf(request):
    syllabus = Syllabus.objects.get(pk=1)

    context_dict = simplejson.loads(syllabus.json_data)
    context_dict['college'] = College.objects.get(pk=context_dict['college'])
    context_dict['department'] = Department.objects.get(
        pk=context_dict['department'])
    context_dict['rubric'] = simplejson.loads(
        Rubric.objects.get(pk=context_dict['rubric']).json_data)

    template = get_template('syllabus/pdf.html')
    context = Context(context_dict)
    html = template.render(context)

    pdf_file = generate_pdf(html=html)
    response = HttpResponse(FileWrapper(pdf_file), mimetype='application/pdf')
    response['Content-Disposition'] = 'filename=%s.pdf' % clean_filename(context_dict['syllabusName'])
    pdf_file.seek(0)
    return response


def generate_pdf(html):
    wkhtmltopdf_default = 'wkhtmltopdf-heroku'

    # Reference command
    # wkhtmltopdf_cmd = environ.get('WKHTMLTOPDF_CMD', wkhtmltopdf_default)
    wkhtmltopdf_cmd = wkhtmltopdf_default

    # Set up return file
    pdf_file = NamedTemporaryFile(delete=False, suffix='.pdf')

    # Save the HTML to a temp file
    html_file = NamedTemporaryFile(delete=False, suffix='.html')
    html_file.write(html)
    html_file.close()

    # wkhtmltopdf
    command = [
        wkhtmltopdf_cmd,
        '-q',
        '--footer-right', 'Page [page]',
        '--margin-bottom', '1in',
        '--margin-left', '1in',
        '--margin-right', '1in',
        '--margin-top', '1in',
        html_file.name,
        pdf_file.name
    ]

    # print list2cmdline(command)
    call_subprocess(command)
    # call_subprocess([command, html_file.name, pdf_file.name])

    return pdf_file

def clean_filename(filename):
    import string
    valid_chars = "-_.()%s%s" % (string.ascii_letters, string.digits)
    return ''.join(c for c in filename if c in valid_chars)
