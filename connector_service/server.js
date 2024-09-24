import express from 'express';
import dotenv from 'dotenv';

dotenv.config();

const app = express();
const port = process.env.PORT || 3000;

app.use(express.json());

app.get('/', (req, res) => {
  res.send('Connector service is running!');
});

app.listen(port, () => {
  console.log(`Connector service listening at http://localhost:${port}`);
});