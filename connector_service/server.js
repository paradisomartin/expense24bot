import app from "./src/app.js";
import config from "./src/config/index.js";
import telegramService from "./src/services/telegramService.js";
import axios from "axios";

const wait = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

const checkBotService = async () => {
  for (let i = 0; i < 10; i++) {
    try {
      console.log(
        `Attempting to connect to bot service at ${config.botServiceUrl}`,
      );
      const response = await axios.get(`${config.botServiceUrl}`);
      console.log(
        `Received response from bot service: ${response.status} ${response.statusText}`,
      );
      if (response.status === 200) {
        console.log("Bot service is ready");
        return;
      }
    } catch (error) {
      console.log(
        `Error connecting to bot service (attempt ${i + 1}):`,
        error.message,
      );
    }
    await wait(5000);
  }
  throw new Error("Bot service is not available after multiple attempts");
};

const startServer = async () => {
  try {
    console.log("Starting connector service...");
    await checkBotService();
    console.log("Bot service check completed");

    console.log("Setting up Telegram webhook...");
    await telegramService.setWebhook();
    console.log("Telegram webhook set up completed");

    app.listen(config.port, () => {
      console.log(
        `Connector Service listening at http://localhost:${config.port}`,
      );
    });
  } catch (error) {
    console.error("Failed to start server:", error);
    // Instead of exiting, let's keep the process running to see logs
    console.log(
      "Server startup failed, but keeping process alive for debugging",
    );
  }
};

console.log("Initializing connector service...");
startServer().catch((error) => {
  console.error("Unhandled error during server startup:", error);
});

// Keep the process running
setInterval(() => {}, 1000);
