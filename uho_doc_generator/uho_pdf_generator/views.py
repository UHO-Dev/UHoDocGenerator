import json
from django.http import FileResponse, HttpResponse
from xhtml2pdf import pisa
from django.template import Context, Template
from django.views import View
from io import BytesIO
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name='dispatch')
class GeneratePDF(View):
    def post(self, request, *args, **kwargs):
        try:
            body_unicode = request.body.decode('utf-8')  # Decode the request body
            body = json.loads(body_unicode)  # Parse the body as JSON

            template = Template(body.get('html'))  # Get HTML template from JSON body
            data = body.get('data', {})  # Get data from JSON body
            
            html = template.render(Context(data))
            result = BytesIO()
            encoded_html = html.encode("ISO-8859-1")
            pdf = pisa.pisaDocument(BytesIO(encoded_html), result)
            if not pdf.err:
                result.seek(0)
                return FileResponse(result, content_type='application/pdf')
            else:
                return HttpResponse('Error Rendering PDF', status=400)
        except Exception as e:
            return HttpResponse(f'Error: {str(e)}', status=400)