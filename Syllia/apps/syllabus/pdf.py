from wsgiref.util import FileWrapper
from os import environ
from subprocess import call as call_subprocess
from tempfile import NamedTemporaryFile

from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import Http404

from Syllia.apps.syllabus.models import College, Department, Rubric

@csrf_protect
@login_required
def return_a_pdf(request):
    if request.method == "POST":
        current_user = get_user_model().objects.get(
            email=request.user.email)

        # If you don't own it, you can't download it
        try:
            syllabus = current_user.syllabus_set.get(pk=request.POST['pk'])

        except Exception:
            raise Http404

        pdf_file = generate_pdf(syllabus=syllabus)
        response = HttpResponse(FileWrapper(pdf_file), mimetype='application/pdf')
        response['Content-Disposition'] = 'filename=%s.pdf' % clean_filename(syllabus.json_data['syllabusName'])
        pdf_file.seek(0)
        return response

    raise Http404


def generate_pdf(syllabus):
    context_dict = syllabus.json_data
    context_dict['college'] = College.objects.get(pk=context_dict['college'])
    context_dict['department'] = Department.objects.get(
        pk=context_dict['department'])
    context_dict['rubric'] = Rubric.objects.get(pk=context_dict['rubric']).json_data

    template = get_template('syllabus/pdf.html')
    context = Context(context_dict)
    html = template.render(context)

    wkhtmltopdf_default = 'wkhtmltopdf-heroku'

    # Reference command
    wkhtmltopdf_cmd = environ.get('WKHTMLTOPDF_CMD', wkhtmltopdf_default)
    # wkhtmltopdf_cmd = wkhtmltopdf_default

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
        '--footer-right', '[page]',
        '--footer-font-name', 'Times',
        '--margin-bottom', '1in',
        '--margin-left', '1in',
        '--margin-right', '1in',
        '--margin-top', '1in',
        '--disable-smart-shrinking',
        html_file.name,
        pdf_file.name
    ]

    call_subprocess(command)

    return pdf_file

def clean_filename(filename):
    import string
    valid_chars = "-_.()%s%s" % (string.ascii_letters, string.digits)
    return ''.join(c for c in filename if c in valid_chars)
