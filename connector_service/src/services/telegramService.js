import TelegramBot from "node-telegram-bot-api";
import config from "../config/index.js";
import { handleMessage } from "../controllers/telegramController.js";

const bot = new TelegramBot(config.telegramToken);

export default {
  async setWebhook() {
    try {
      await bot.setWebHook(
        `${config.webhookUrl}/telegram/webhook/${config.telegramToken}`,
      );
      console.log("Webhook set successfully");
    } catch (error) {
      console.error("Error setting webhook:", error);
    }
  },

  async processUpdate(update) {
    if (update.message) {
      const chatId = update.message.chat.id;
      const text = update.message.text;
      await handleMessage(chatId, text);
    }
  },

  async sendMessage(chatId, text) {
    await bot.sendMessage(chatId, text);
  },
};
