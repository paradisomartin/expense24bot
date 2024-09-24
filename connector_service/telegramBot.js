import TelegramBot from "node-telegram-bot-api";
import { TELEGRAM_BOT_TOKEN, BOT_SERVICE_URL } from "./config.js";
import axios from "axios";

const bot = new TelegramBot(TELEGRAM_BOT_TOKEN, { polling: true });

const getUsernameOrError = (msg) => {
  if (!msg.from.username) {
    throw new Error("No username");
  }
  return msg.from.username;
};

const sendMessageToBotService = async (username, messageText) => {
  console.log(`Sending request to Bot Service at: ${BOT_SERVICE_URL}`);
  try {
    const response = await axios.post(BOT_SERVICE_URL, {
      message: messageText,
      telegram_id: username,
    });
    return response.data.response;
  } catch (error) {
    if (error.response && error.response.status === 403) {
      throw new Error("Unauthorized user");
    }
    throw error;
  }
};

const handleError = async (chatId, error) => {
  console.error("Error:", error.message);
  console.error("Full error object:", JSON.stringify(error, null, 2));

  let errorMessage;
  switch (error.message) {
    case "No username":
      errorMessage = "You must set up a username in Telegram to use this Bot.";
      break;
    case "Unauthorized user":
      errorMessage =
        "You are not authorized to use this Bot. Please contact the administrator.";
      break;
    default:
      errorMessage = "Sorry, there was an error processing your message.";
  }

  await bot.sendMessage(chatId, errorMessage);
};

bot.on("message", async (msg) => {
  const chatId = msg.chat.id;
  const messageText = msg.text;

  try {
    const username = getUsernameOrError(msg);
    console.log(`Received message from ${username}: ${messageText}`);

    const responseMessage = await sendMessageToBotService(
      username,
      messageText,
    );
    await bot.sendMessage(chatId, responseMessage);
  } catch (error) {
    await handleError(chatId, error);
  }
});

console.log("Telegram bot is running with polling.");
