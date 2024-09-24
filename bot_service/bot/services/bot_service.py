from bot.models import TelegramUser, Expense
import re

class BotService:
    def __init__(self):
        self.expense_categories = {
            "Vivienda": ["renta", "alquiler", "hipoteca", "casa", "departamento", "electricidad", "agua", "gas"],
            "Transporte": ["gasolina", "transporte", "uber", "taxi", "bus", "metro", "combustible", "estacionamiento", "peaje"],
            "Alimentación": ["comida", "restaurante", "supermercado", "pizza", "hamburguesa", "grocery", "alimentos", "cena", "almuerzo", "desayuno", "café", "helado", "fruta", "verdura"],
            "Servicios": ["luz", "agua", "gas", "internet", "teléfono", "cable", "streaming"],
            "Seguros": ["seguro", "póliza", "aseguranza"],
            "Salud": ["médico", "doctor", "hospital", "medicinas", "farmacia", "dentista", "psicólogo"],
            "Ahorros": ["ahorro", "inversión", "depósito"],
            "Deudas": ["deuda", "préstamo", "tarjeta de crédito", "crédito"],
            "Educación": ["colegio", "universidad", "libro", "curso", "escuela", "matrícula", "útiles"],
            "Entretenimiento": ["cine", "concierto", "juego", "fiesta", "diversión", "teatro", "museo", "viaje", "vacaciones"],
            "Ropa": ["ropa", "zapatos", "accesorios", "joyería"],
            "Tecnología": ["computadora", "celular", "tablet", "gadget", "electrónica"],
            "Mascotas": ["mascota", "veterinario", "comida para mascotas"],
            "Otros": []
        }

    def is_user_whitelisted(self, telegram_id):
        """Verifica si el usuario está en la lista blanca."""
        return TelegramUser.objects.filter(telegram_id=telegram_id).exists()

    def process_message(self, telegram_id, message):
        """Procesa el mensaje del usuario y añade el gasto si es válido."""
        expense_info = self.parse_expense(message)
        if expense_info:
            return self.add_expense(telegram_id, expense_info)
        else:
            return "Mensaje no reconocido como un gasto"

    def parse_expense(self, message):
        """Extrae la información del gasto del mensaje."""
        pattern = r"(.*?)\s+(\d+(?:\.\d{1,2})?)\s*(pesos|dólares?|usd)?$"
        match = re.match(pattern, message, re.IGNORECASE)
        if match:
            description = match.group(1).strip()
            amount = float(match.group(2))
            currency = match.group(3) if match.group(3) else "pesos"
            return {"description": description, "amount": amount, "currency": currency}
        return None

    def add_expense(self, telegram_id, expense_info):
        """Añade el gasto a la base de datos."""
        user = TelegramUser.objects.get(telegram_id=telegram_id)
        category = self.categorize_expense(expense_info['description'])
        
        Expense.objects.create(
            user=user,
            description=expense_info['description'],
            amount=expense_info['amount'],
            category=category
        )
        
        return f"Gasto de {category} añadido: {expense_info['amount']} {expense_info['currency']} ✅"

    def categorize_expense(self, description):
        """Categoriza el gasto basándose en la descripción."""
        description_lower = description.lower()
        for category, keywords in self.expense_categories.items():
            if any(keyword in description_lower for keyword in keywords):
                return category
        return "Otros"