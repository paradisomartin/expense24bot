import dotenv from "dotenv";

dotenv.config();

export default {
  telegramToken: process.env.TELEGRAM_BOT_TOKEN,
  webhookUrl: process.env.WEBHOOK_URL,
  botServiceUrl: process.env.BOT_SERVICE_URL || "http://bot_service:5001",
  port: process.env.PORT || 3000,
};
