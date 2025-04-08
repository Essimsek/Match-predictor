import express, {Request, Response} from 'express';
import dotenv from 'dotenv';
import axios from 'axios';

dotenv.config();

const flaskBackendUrl = process.env.FLASK_BACKEND_URL;
const app = express();
const port = 3000;

app.get('/api/standings', async (req: Request, res: Response) => {
    const response = await axios.get (`${flaskBackendUrl}/api-flask/standings`);
    const data = response.data;
    res.json(data);
});

app.listen(port, () => {
    console.log(`Example app listening on port ${port}`);
});