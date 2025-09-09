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

app.listen(port, '0.0.0.0', () => {
    console.log(`Backend listening on 0.0.0.0:${port}`);
  });