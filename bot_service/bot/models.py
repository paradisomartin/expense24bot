from django.db import models

class TelegramUser(models.Model):
    telegram_id = models.TextField(unique=True)

    def __str__(self):
        return f"TelegramUser: {self.telegram_id}"

class Expense(models.Model):
    user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE)
    description = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.TextField()
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.description} - {self.amount}"