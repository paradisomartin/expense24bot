from rest_framework.views import APIView
from rest_framework.response import Response
from .services.bot_service import BotService
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from django.conf import settings

class ProcessMessageView(APIView):
    def post(self, request):
        message = request.data.get('message')
        telegram_id = request.data.get('telegram_id')

        bot_service = BotService()

        # Inicializar LangChain
        llm = OpenAI(temperature=0, openai_api_key=settings.OPENAI_API_KEY)
        prompt = PromptTemplate(
            input_variables=["message"],
            template="Analiza si este mensaje describe un gasto. Si es así, extrae el monto y la categoría. Si no es un gasto, responde normalmente: {message}"
        )
        chain = LLMChain(llm=llm, prompt=prompt)

        # Procesar el mensaje con LangChain
        response = chain.run(message)

        # Por ahora, simplemente devolvemos la respuesta de LangChain
        return Response({"response": response})