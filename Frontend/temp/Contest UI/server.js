const express = require('express');
const bodyParser = require('body-parser');
const createCsvWriter = require('csv-writer').createObjectCsvWriter;
const path = require('path');
const fs = require('fs');

const app = express();
const port = 3000;

// Middleware
app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static('public'));

// CSV Writer setup
const csvWriter = createCsvWriter({
    path: 'contests.csv',
    header: [
        { id: 'contestName', title: 'Contest Name' },
        { id: 'startTime', title: 'Start Time' },
        { id: 'endTime', title: 'End Time' },
        { id: 'organizationType', title: 'Organization Type' },
        { id: 'organizationName', title: 'Organization Name' }
    ],
    append: true
});

// Create CSV file with headers if it doesn't exist
if (!fs.existsSync('contests.csv')) {
    csvWriter.writeRecords([]);
}

// Routes
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.post('/submit', async (req, res) => {
    try {
        const formData = {
            contestName: req.body.contestName,
            startTime: `${req.body.startDate} ${req.body.startTime}`,
            endTime: req.body.noEndTime ? 'No End Time' : `${req.body.endDate} ${req.body.endTime}`,
            organizationType: req.body.organizationType,
            organizationName: req.body.organizationName
        };

        await csvWriter.writeRecords([formData]);
        res.send(`
            <html>
                <head>
                    <style>
                        body { 
                            font-family: Arial, sans-serif;
                            display: flex;
                            justify-content: center;
                            align-items: center;
                            height: 100vh;
                            margin: 0;
                            background-color: #f5f5f5;
                        }
                        .message {
                            text-align: center;
                            padding: 20px;
                            background: white;
                            border-radius: 8px;
                            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                        }
                        .button {
                            display: inline-block;
                            padding: 10px 20px;
                            background-color: #4CAF50;
                            color: white;
                            text-decoration: none;
                            border-radius: 4px;
                            margin-top: 15px;
                        }
                    </style>
                </head>
                <body>
                    <div class="message">
                        <h2>Contest Created Successfully!</h2>
                        <p>Your contest details have been saved.</p>
                        <a href="/" class="button">Create Another Contest</a>
                    </div>
                </body>
            </html>
        `);
    } catch (error) {
        res.status(500).send('Error saving contest data');
    }
});

app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});
