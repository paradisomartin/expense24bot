import dotenv from "dotenv";

dotenv.config();

export const { CONNECTOR_SERVICE_PORT, TELEGRAM_BOT_TOKEN, BOT_SERVICE_URL } =
  process.env;

export const PORT = CONNECTOR_SERVICE_PORT || 3000;
