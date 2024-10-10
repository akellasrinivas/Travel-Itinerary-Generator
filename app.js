const express = require('express');
const { exec } = require('child_process');
const path = require('path');
const bodyParser = require('body-parser');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());
app.use(express.static(path.join(__dirname, 'public'))); // Serve static files from 'public' directory

// Endpoint to generate itinerary
app.post('/generate-itinerary', (req, res) => {
    const { place } = req.body;

    exec(`python scripts/itinerary.py "${place}"`, (error, stdout, stderr) => {
        if (error) {
            console.error(`Error executing Python script: ${error}`);
            return res.status(500).send({ error: "Error generating itinerary." });
        }

        try {
            const itineraryInfo = JSON.parse(stdout);
            res.json(itineraryInfo);
        } catch (parseError) {
            console.error(`Error parsing Python output: ${parseError}`);
            res.status(500).send({ error: "Error parsing itinerary response." });
        }
    });
});

// Serve the index.html file
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Start the server
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
