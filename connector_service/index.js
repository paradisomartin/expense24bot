import dotenv from "dotenv";
import TelegramBot from "node-telegram-bot-api";
import { Configuration, OpenAIApi } from "openai";

dotenv.config();

const TELEGRAM_BOT_TOKEN = process.env.TELEGRAM_BOT_TOKEN;
const OPENAI_API_KEY = process.env.OPENAI_API_KEY;

async function testTelegramConnection() {
  try {
    const bot = new TelegramBot(TELEGRAM_BOT_TOKEN);
    const botInfo = await bot.getMe();
    console.log(
      `Telegram connection successful. Bot name: ${botInfo.first_name}`,
    );
  } catch (error) {
    console.error("Error connecting to Telegram:", error.message);
  }
}

async function testOpenAIConnection() {
  try {
    const configuration = new Configuration({
      apiKey: OPENAI_API_KEY,
    });
    const openai = new OpenAIApi(configuration);
    const response = await openai.createCompletion({
      model: "text-davinci-002",
      prompt: "Hello, World!",
      max_tokens: 5,
    });
    console.log(
      "OpenAI connection successful. Response:",
      response.data.choices[0].text.trim(),
    );
  } catch (error) {
    console.error("Error connecting to OpenAI:", error.message);
  }
}

async function runTests() {
  console.log("Testing connections...");
  await testTelegramConnection();
  await testOpenAIConnection();
  console.log("Connection tests completed.");
}

runTests();
