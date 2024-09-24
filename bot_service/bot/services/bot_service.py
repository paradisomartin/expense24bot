from bot.models import User, Expense
import re

class BotService:
    def __init__(self):
        pass

    def is_user_whitelisted(self, telegram_id):
        return User.objects.filter(telegram_id=telegram_id).exists()

    def process_message(self, telegram_id, message):
        if not self.is_user_whitelisted(telegram_id):
            return "User not authorized"

        expense_info = self.parse_expense(message)
        if expense_info:
            return self.add_expense(telegram_id, expense_info)
        else:
            return "Message not recognized as an expense"

    def parse_expense(self, message):
        # Patrón básico: "descripción monto"
        pattern = r"(.*?)\s+(\d+(?:\.\d{1,2})?)\s*(?:bucks|dollars?|usd)?$"
        match = re.match(pattern, message, re.IGNORECASE)
        if match:
            description = match.group(1).strip()
            amount = float(match.group(2))
            return {"description": description, "amount": amount}
        return None

    def add_expense(self, telegram_id, expense_info):
        user = User.objects.get(telegram_id=telegram_id)
        category = self.categorize_expense(expense_info['description'])
        
        expense = Expense.objects.create(
            user=user,
            description=expense_info['description'],
            amount=expense_info['amount'],
            category=category
        )
        
        return f"{category} expense added ✅"

    def categorize_expense(self, description):
        # Implementación básica, se mejorará con LangChain
        categories = ["Housing", "Transportation", "Food", "Utilities", "Insurance", 
                      "Medical/Healthcare", "Savings", "Debt", "Education", "Entertainment"]
        
        for category in categories:
            if category.lower() in description.lower():
                return category
        return "Other"