from rest_framework.views import APIView
from rest_framework.response import Response
from .services.bot_service import BotService
from langchain.llms import Cohere
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from django.conf import settings

class ProcessMessageView(APIView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bot_service = BotService()
        self.llm_chain = self._initialize_llm_chain()

    def _initialize_llm_chain(self):
        cohere = Cohere(
            cohere_api_key=settings.COHERE_API_KEY,
            model='command',
            max_tokens=300,
            temperature=0.7
        )
        
        prompt = PromptTemplate(
            input_variables=["message"],
            template="Analiza si este mensaje describe un gasto. Si es así, extrae el monto y la categoría. No modifiques el texto original del gasto. Responde en español. Si no es un gasto, responde normalmente: {message}"
        )
        
        return LLMChain(llm=cohere, prompt=prompt)

    def post(self, request):
        message = request.data.get('message')
        telegram_id = request.data.get('telegram_id')

        if not telegram_id:
            return Response({"error": "Se requiere telegram_id"}, status=400)

        if not self.bot_service.is_user_whitelisted(telegram_id):
            return Response({"response": "Usuario no autorizado"}, status=403)

        llm_response = self.llm_chain.run(message)
        bot_response = self.bot_service.process_message(telegram_id, message)  # Usa el mensaje original, no la respuesta del LLM

        return Response({
            "llm_response": llm_response.strip(),
            "bot_response": bot_response.strip()
        })