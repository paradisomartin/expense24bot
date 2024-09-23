import telegramService from "../services/telegramService.js";
import botService from "../services/botService.js";

export const handleWebhook = async (req, res) => {
  const update = req.body;
  await telegramService.processUpdate(update);
  res.sendStatus(200);
};

export const handleMessage = async (chatId, text) => {
  try {
    console.log(`Handling message: chatId=${chatId}, text=${text}`);
    const response = await botService.sendMessage(chatId, text);
    console.log("Response from bot service:", response);

    if (response && response.response) {
      await telegramService.sendMessage(chatId, response.response);
    } else {
      console.error("Unexpected response format from bot service:", response);
      await telegramService.sendMessage(
        chatId,
        "Sorry, I couldn't process your message.",
      );
    }
  } catch (error) {
    console.error("Error handling message:", error);
    await telegramService.sendMessage(
      chatId,
      "Sorry, there was an error processing your message.",
    );
  }
};
