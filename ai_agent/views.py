from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .openai_client import get_openai_client


class Alerts(APIView):

    def get(self, request, format=None):
        return Response({
            'Alert': {
                'content': {
                    'new_invoices': 54,
                    'new_duplicate_invoices': 12,
                            },
                'type': "duplicated",
                'message': "The Canada Customs & Revenue Agency has 9 new invoices with a high confidence level of being duplicated. I recommend reviewing these invoices.",
                'UUID': '173cc4a2d7b9fc54dc35b9951cc28a7308b9b394bc09fc7544134a0f015d19e6',
                },
        })

class AiAssistant(APIView):
    conversation_history = [
        {"role": "system", "content": "You are a helpful assistant called Sofia. You were designed by the company Ofiservices to help with process mining analysis. Your main function is to give the user meaningful insights and advice about the processes in the system."},
        {"role": "system", "content": "Each case has this information: id (a number between 1 and 1000), type (can be Renewal, Policy onboarding or Issuance), branch (a number between 1 and 10), ramo (Crop Insurance, Marine Insurance, Travel Insurance, Pet Insurance, Life Insurance, Auto Insurance), brocker (Sean, Priscilla, Courtney, Edward, Darlene, Tamara, Hazel, Ralph, Miranda, Todd, Matthew, Sophia, Eva, Dean), client (Sean, Priscilla, Courtney, Edward, Darlene, Tamara, Hazel, Ralph, Miranda, Todd, Matthew, Sophia, Eva, Dean), creator (Sean, Priscilla, Courtney, Edward, Darlene, Tamara, Hazel, Ralph, Miranda, Todd, Matthew, Sophia, Eva, Dean)."},
        {"role": "system", "content": "Always give some advice or recommendation to the user."},
        {"role": "system", "content": "When asked something you don't know, you make something up. You never say you dont know or that you cant access data. If asked with a specific number or data you return a random number which makes sense."},
        {"role": "system", "content": "This is the list of processes (also called activities): Registro de compromiso, Enviar a Revisión suscripción, Validar info enviada, Reasignacion a suscriptor de mayor nivel, Devolver caso a Comercial, Aprobar solicitud en suscripcion local, Enviar respuesta al area comercial, Aceptar (ganado) por parte del Brocker, Visado, Devolucion a comercial desde visado, Revisión en emisión, Iniciar facturación, Generar Factura, Contabilizar Factura, Generar poliza, Enviar factura electronica, Respuesta SRI, Enviar poliza electronica, Firma poliza electronica por parte del cliente, Finalizar envio poliza y factura al cliente, Finalizar proceso de emision, Recepcion pago, Rechazar (perdida) por parte del Brocker, Ingresar tramite, Registrar PO, Enviar a emision, Realizar devolucion desde suscripcion, Control de calidad documental, Devolucion a emision de control de calidad, Devolucion a emision, Declinar solicitud en suscripcion, Devolucion a comercial desde emisión, Devolucion al brocker del caso (Revision Brocker), Declinar por parte del Brocker, Devolucion a comercial (corregir informacion), Devolucion a visado desde emisión"}, 
        {"role": "system", "content": "Always start by introducing yourself"},
        {"role": "system", "content": "Each activity has an average time of around half a hour."},
        {"role": "system", "content": "There are 290 variants , a variant is a list of processes that a case goes through from its creation to its resolution."},
    ]

    def message_openai(self, message):
        try:
            client = get_openai_client()
            self.conversation_history.append({"role": "user", "content": message})
            completion = client.chat.completions.create(
                model="gpt-4o",
                messages=self.conversation_history
            )
            return completion.choices[0].message.content
        except Exception as e:
            print(f"Error communicating with OpenAI: {e}")
            return "Sorry, I couldn't process your request at the moment."

    def post(self, request, format=None):
        try:
            data = request.data
            message = data.get('message')
            response = self.message_openai(message)
            return Response({'response': response})
        except Exception as e:
            print(f"Error processing request: {e}")
            return Response({"error": str(e)}, status=500)