from collections import OrderedDict
from threading import Thread

from django.template.loader import render_to_string
from django.utils.html import strip_tags

from students.models import Student


def send_student_email(self, student, subject, template_name, context):

    html_content = render_to_string(template_name=template_name, context=context)
    plain_message = strip_tags(html_content)

    thread = Thread(
        target=student.email_student,
        kwargs={
            "subject": subject,
            "message": plain_message,
            "html_message": html_content,
        },
    )
    thread.start()


def send_email(self, student_id: int, subject: str, serializer_data: OrderedDict):
    message = serializer_data.get("message")

    student = Student.objects.get(id=student_id)

    context = {
        "name": student.user.first_name,
        "message": message,
    }

    self.send_customer_email(student, subject, "email_wec_freight_update.html", context)
