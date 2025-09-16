import express, {Request, Response} from 'express';
import dotenv from 'dotenv';
import axios from 'axios';
import cors from "cors";

dotenv.config();

const flaskBackendUrl = process.env.FLASK_BACKEND_URL;
const app = express();
const port = 3000;
app.use(cors({
    origin: [
      'http://localhost:5173',
      //'http://frontend:5173',
    ],
    credentials: true
  }));


app.get('/api/standings', async (req: Request, res: Response) => {
    const response = await axios.get (`${flaskBackendUrl}/api-flask/standings`);
    const data = await response.data;
    res.json(data);
});

app.get('/api/predict', async (req: Request, res: Response) => {
    setTimeout(() => {}, 2000);
    try {
        const { home = 'Galatasaray', away = 'Fenerbahce' } = req.query as { home?: string; away?: string };

        const response = await axios.get(`${flaskBackendUrl}/api-flask/predict`, {
            params: { home, away }
        });

        const data = response.data;
        console.log("Prediction data: ", data);
        res.json(data);
    } catch (error) {
        console.error(error);
        res.status(500).json({ error: "Something went wrong" });
    }
});

app.get('/api/fixtures', async (req: Request, res: Response) => {
    const response = await axios.get(`${flaskBackendUrl}/api-flask/fixtures`);
    const data = await response.data;
    res.json(data);
});

app.listen(port, '0.0.0.0', () => {
    console.log(`Backend listening on 0.0.0.0:${port}`);
  });