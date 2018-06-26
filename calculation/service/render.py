# -*- coding: utf-8 -*-
import os
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
import xhtml2pdf.pisa as pisa
from io import StringIO
from django.conf import settings

def fetch_pdf_resources(uri, rel):
    if settings.STATIC_URL and uri.startswith(settings.STATIC_URL):
        path = os.path.join(settings.STATIC_ROOT, uri.replace(settings.STATIC_URL,""))
        print(str(path))
        return path
    elif settings.MEDIA_URL and uri.startswith(settings.MEDIA_URL):
        print(2)
        path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ""))
    else:
        print(3)
        path = os.path.join(settings.STATIC_ROOT, uri)

    print('path')
    return path


class Render:

    @staticmethod
    def render(path: str, params: dict):
        template = get_template(path)
        html = template.render(params)

        response = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), response, encoding='utf-8',
                                                           link_callback=fetch_pdf_resources)
        if not pdf.err:
            return HttpResponse(response.getvalue(), content_type='application/pdf')
        else:
            return HttpResponse("Error Rendering PDF", status=400)

    @staticmethod
    def _render(path: str, params: dict):
        template = get_template(path)
        html = template.render(params)
        response = HttpResponse(content_type='application/pdf')
        pisaStatus = pisa.CreatePDF(html, dest=response,
                                    link_callback=fetch_pdf_resources)
        # if error then show some funy view
        if pisaStatus.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response
