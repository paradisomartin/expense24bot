import axios from "axios";
import config from "../config/index.js";

export default {
  async sendMessage(chatId, text) {
    try {
      console.log(
        `Sending message to bot service: chatId=${chatId}, text=${text}`,
      );
      const response = await axios.post(`${config.botServiceUrl}/message`, {
        chatId,
        text,
      });
      console.log("Response from bot service:", response.data);
      return response.data;
    } catch (error) {
      console.error("Error sending message to bot service:", error.message);
      throw error;
    }
  },
};
