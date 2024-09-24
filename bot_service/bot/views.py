from rest_framework.views import APIView
from rest_framework.response import Response
from .services.bot_service import BotService
from langchain.llms import Cohere
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from django.conf import settings

class ProcessMessageView(APIView):
    def post(self, request):
        message = request.data.get('message')
        telegram_id = request.data.get('telegram_id')

        bot_service = BotService()

        # Inicializar LangChain con Cohere
        cohere = Cohere(
            cohere_api_key=settings.COHERE_API_KEY,
            model='command',  # Especificamos el modelo de Cohere a usar
            max_tokens=300,   # Limitamos la longitud de la respuesta
            temperature=0.7   # Ajustamos la creatividad de la respuesta
        )
        prompt = PromptTemplate(
            input_variables=["message"],
            template="Analiza si este mensaje describe un gasto. Si es así, extrae el monto y la categoría. Responde en español. Si no es un gasto, responde normalmente: {message}"
        )
        chain = LLMChain(llm=cohere, prompt=prompt)

        # Procesar el mensaje con LangChain
        response = chain.run(message)

        # Devolvemos la respuesta de LangChain
        return Response({"response": response.strip()})