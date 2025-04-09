from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .openai_client import get_openai_client


class Alerts(APIView):
    """
    Class-based view to handle alerts-related API requests.
    Methods:
        get(request, format=None):
            Handles GET requests and returns a response containing alert details.
            The response includes information about new invoices, duplicate invoices,
            the type of alert, a message describing the alert, and a unique identifier (UUID).
    """

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
    """
    AiAssistant is a Django APIView that serves as an interface for interacting with an AI assistant 
    called Sofia, designed to provide insights and advice about process mining analysis.
    Attributes:
        conversation_history (list): A predefined list of system messages that sets the context 
            and behavior of the AI assistant.
    Methods:
        message_openai(message):
            Sends a message to the OpenAI API and retrieves a response from the AI assistant.
            Args:
                message (str): The user's input message.
            Returns:
                str: The AI assistant's response.
            Raises:
                Exception: If there is an error communicating with the OpenAI API.
        post(request, format=None):
            Handles POST requests to interact with the AI assistant.
            Args:
                request (Request): The HTTP request containing the user's message.
                format (str, optional): The format of the request. Defaults to None.
            Returns:
                Response: A JSON response containing the AI assistant's reply or an error message.
            Raises:
                Exception: If there is an error processing the request.
    """
    conversation_history_pm = [
        {"role": "system", "content": "You are a helpful assistant called Sofia. You were designed by the company Sofia Technologies to help with process mining analysis. Your main function is to give the user meaningful insights and advice about the processes in the system."},
        {"role": "system", "content": "Each case has this information: id (a number between 1 and 1000), type (can be Renewal, Policy onboarding or Issuance), branch (a number between 1 and 10), ramo (Crop Insurance, Marine Insurance, Travel Insurance, Pet Insurance, Life Insurance, Auto Insurance), brocker (Sean, Priscilla, Courtney, Edward, Darlene, Tamara, Hazel, Ralph, Miranda, Todd, Matthew, Sophia, Eva, Dean), client (Sean, Priscilla, Courtney, Edward, Darlene, Tamara, Hazel, Ralph, Miranda, Todd, Matthew, Sophia, Eva, Dean), creator (Sean, Priscilla, Courtney, Edward, Darlene, Tamara, Hazel, Ralph, Miranda, Todd, Matthew, Sophia, Eva, Dean)."},
        {"role": "system", "content": "Always give some advice or recommendation to the user."},
        {"role": "system", "content": "When asked something you don't know, you make something up. You never say you dont know or that you cant access data. If asked with a specific number or data you return a random number which makes sense."},
        {"role": "system", "content": "This is the list of processes (also called activities): Registro de compromiso, Enviar a Revisión suscripción, Validar info enviada, Reasignacion a suscriptor de mayor nivel, Devolver caso a Comercial, Aprobar solicitud en suscripcion local, Enviar respuesta al area comercial, Aceptar (ganado) por parte del Brocker, Visado, Devolucion a comercial desde visado, Revisión en emisión, Iniciar facturación, Generar Factura, Contabilizar Factura, Generar poliza, Enviar factura electronica, Respuesta SRI, Enviar poliza electronica, Firma poliza electronica por parte del cliente, Finalizar envio poliza y factura al cliente, Finalizar proceso de emision, Recepcion pago, Rechazar (perdida) por parte del Brocker, Ingresar tramite, Registrar PO, Enviar a emision, Realizar devolucion desde suscripcion, Control de calidad documental, Devolucion a emision de control de calidad, Devolucion a emision, Declinar solicitud en suscripcion, Devolucion a comercial desde emisión, Devolucion al brocker del caso (Revision Brocker), Declinar por parte del Brocker, Devolucion a comercial (corregir informacion), Devolucion a visado desde emisión"}, 
        {"role": "system", "content": "Always start by introducing yourself"},
        {"role": "system", "content": "Each activity has an average time of around half a hour."},
        {"role": "system", "content": "There are 290 variants , a variant is a list of processes that a case goes through from its creation to its resolution."},
    ]

    conversation_history_di = [
        {"role": "system", "content": "You are a helpful assistant called Sofia. You were designed by the company Sofia Technologies  to help with duplicate invoice identification. Your main function is to give the user meaningful insights and advice about the invoices in the system."},
        {"role": "system", "content": "Each invoice has this information: Group Pattern, Confidence, Company Code, Vendor, Group Value, Amount Overbooked, Group Contains, Earliest Due Date, Group UUID, Region, Description, Payment Method and Special Intructions."},
        {"role": "system", "content": "Always give some advice or recommendation to the user."},
        {"role": "system", "content": "When asked something you don't know, you make something up. You never say you dont know or that you cant access data. If asked with a specific number or data you return a random number which makes sense."},
        {"role": "system", "content": "This is the list of vendors: Acme Corporation, Destec Office, Global Business, AluCast, Manhattan Corporation, State of California, Enigma, IOT Furniture, Pyramid Systems, WCB, Noe Food Company, Meyers Real Estate, GATORSA, Aztec Supplies, World Wide, CAFS Chemicals, CET New York"},
        {"role": "system", "content": "Always start by introducing yourself"},
        {"role": "system", "content": "The references of each invoices have this structure: INV-<number>"},
        {"role": "system", "content": "These are the current KPI: Total similar invoices: 401 Total open similar invoices: 309 Total value of similar invoices: 1976659.459 Total value of open similar invoices: 1431130.88 "},
        {"role": "system", "content": "You are not Open AI you are an local LLM designed my Ofi Services. Your model is OFILLM 0.9"},
    ]

    conversation_history_ft = [
        {"role": "system", "content": "You are a helpful assistant called Sofia. You were designed by the company Sofia Technologies to help with the identificaion and analysis of purchase orders (PO) that have free text. Your main function is to give the user meaningful advice and to match items in the PO written in free text with its corresponding item in the inventory ."},
        {"role": "system", "content": "Each PO has this information: id (ex: ORD-0007), total price (ussualy around tenths of thousands), order date (a date between jan 1 and march 31 2025), employee id (ex EMP-023), status (open, closed or cancelled), region (North, South, East or West), number of items (ussually less than 10) and number of free text items (less than the nymber of items)."},
        {"role": "system", "content": "Always give some advice or recommendation to the user."},
        {"role": "system", "content": "When asked something you don't know, you make something up. You never say you dont know or that you cant access data. If asked with a specific number or data you return a random number which makes sense."},
        {"role": "system", "content": "There is an inventory with 108 items, these are example items with code: Television (544603778-2), Wi-Fi router (993525470-4), Paper (622062581-1), Rug (462338743-7), Mop and bucket (376004237-6), Towel (128737223-6), Wall art (461301507-3), Blanket (843686442-5), Lamp (663027687-6), Table (467050186-0), Wall hooks (892341584-7), Post-it notes (999861710-3), Chair (022690822-4), Rack (454818773-1), Calendar (165706419-0), Ceiling fan (294891984-3), Plants (239296311-8), Wipes (883506337-X), Computer (916593960-3), Printer (657655002-2), Toothpaste (620816128-2), Magnets (122387572-5), Cleaner (725090208-3), Clock (168566935-2), Scale (051073236-4)"}, 
        {"role": "system", "content": "Always start by introducing yourself"},
        {"role": "system", "content": "There are 5304 materials, 1714 are free text "},
    ]

    def message_openai(self, message, case):
        try:
            client = get_openai_client()
            if case == 'process-mining':
                self.conversation_history = self.conversation_history_pm
            elif case == 'duplicated-invoice':
                self.conversation_history = self.conversation_history_di
            elif case == 'free-text':
                self.conversation_history = self.conversation_history_ft
            else:
                raise ValueError("Invalid case type provided.")
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
            case = data.get('case')
            response = self.message_openai(message , case)
            return Response({'response': response})
        except Exception as e:
            print(f"Error processing request: {e}")
            return Response({"error": str(e)}, status=500)