from bot.models import TelegramUser, Expense
import re
from django.db.models import Sum
from datetime import datetime, timedelta

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

    def is_expense_message(self, message):
        """Verifica si el mensaje parece ser un gasto."""
        # Patrón para detectar un número seguido de una unidad monetaria
        pattern = r'\d+(?:\.\d{1,2})?\s*(?:pesos|dólares?|usd|€|£|\$)'
        return bool(re.search(pattern, message, re.IGNORECASE))

    def process_message(self, telegram_id, message):
        """Procesa el mensaje del usuario."""
        if not self.is_user_whitelisted(telegram_id):
            return "Usuario no autorizado"

        if message.lower() in ["listar gastos", "listar expensas"]:
            return self.list_expenses(telegram_id)

        if self.is_expense_message(message):
            expense_info = self.parse_expense(message)
            if expense_info:
                return self.add_expense(telegram_id, expense_info)

        return None  # Ignoramos mensajes que no son comandos ni gastos


    def parse_expense(self, message):
        """Extrae la información del gasto del mensaje."""
        pattern = r'(.*?)\s+(\d+(?:\.\d{1,2})?)\s*(pesos|dólares?|usd|€|£|\$)?'
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

        return f"{category} gasto añadido ✅"

    def categorize_expense(self, description):
        """Categoriza el gasto basándose en la descripción."""
        description_lower = description.lower()
        for category, keywords in self.expense_categories.items():
            if any(keyword in description_lower for keyword in keywords):
                return category
        return "Otros"

    def list_expenses(self, telegram_id, period='week'):
        """Lista los gastos del usuario para un período dado."""
        user = TelegramUser.objects.get(telegram_id=telegram_id)

        if period == 'week':
            start_date = datetime.now() - timedelta(days=7)
        elif period == 'month':
            start_date = datetime.now() - timedelta(days=30)
        else:
            return "Período no válido. Use 'week' o 'month'."

        expenses = Expense.objects.filter(user=user, added_at__gte=start_date)

        if not expenses:
            return f"No se encontraron gastos en el último {period}."

        total = expenses.aggregate(Sum('amount'))['amount__sum']

        expense_list = [f"{e.description}: ${e.amount:.2f} ({e.category})" for e in expenses]
        expense_str = "\n".join(expense_list)

        return f"Gastos del último {period}:\n\n{expense_str}\n\nTotal: ${total:.2f}"
