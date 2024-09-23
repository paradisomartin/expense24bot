import express from "express";
import telegramRoutes from "./telegramRoutes.js";

const router = express.Router();

router.use("/telegram", telegramRoutes);

router.get("/", (req, res) => {
  res.send("Connector Service is running");
});

export default router;
