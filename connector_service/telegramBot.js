import TelegramBot from "node-telegram-bot-api";
import { TELEGRAM_BOT_TOKEN } from "./config.js";

const bot = new TelegramBot(TELEGRAM_BOT_TOKEN, { polling: true });

bot.on("message", async (msg) => {
  const chatId = msg.chat.id;
  const messageText = msg.text;

  console.log(`Received message: ${messageText}`);

  try {
    // For now, we'll just echo the message back
    await bot.sendMessage(chatId, `You said: ${messageText}`);
  } catch (error) {
    console.error("Error:", error);
    await bot.sendMessage(
      chatId,
      "Sorry, there was an error processing your message.",
    );
  }
});

export default bot;
