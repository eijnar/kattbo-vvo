require('dotenv').config();
const express = require('express');
const axios = require('axios');
const bodyParser = require('body-parser');

const app = express();
app.use(bodyParser.json());

const CLIENT_ID = "9od4dfbfkw9xvkzvxnkmij2i79zeeawx4dy5";
const CLIENT_SECRET = "d3i4ethiyphqnek34sf8sryam9fygmuymcvk";
const TOKEN_URL = 'http://127.0.0.1:8000/token';

app.post('/exchange-code', async (req, res) => {
    const { code, redirect_uri } = req.body;

    try {
        const response = await axios.post(TOKEN_URL, new URLSearchParams({
            grant_type: 'authorization_code',
            code: code,
            redirect_uri: redirect_uri,
            client_id: CLIENT_ID,
            client_secret: CLIENT_SECRET,
        }), {
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        });

        res.json({ access_token: response.data.access_token });
    } catch (error) {
        console.error('Error exchanging code for token', error);
        res.status(500).json({ error: 'Failed to exchange code for token' });
    }
});

app.listen(8001, () => {
    console.log('Server running on http://localhost:8001');
});
