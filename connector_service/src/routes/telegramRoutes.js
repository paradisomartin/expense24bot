import express from "express";
import { handleWebhook } from "../controllers/telegramController.js";
import config from "../config/index.js";

const router = express.Router();

router.post(`/webhook/${config.telegramToken}`, handleWebhook);

export default router;
