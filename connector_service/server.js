import express from "express";
import { PORT } from "./config.js";
import "./telegramBot.js";

const app = express();

app.use(express.json());

app.get("/", (req, res) => {
  res.send("Connector service is running!");
});

app.listen(PORT, () => {
  console.log(`Connector service listening at http://localhost:${PORT}`);
});
