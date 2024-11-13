// scripts/fetchProblems.js
const fs = require('fs');
const path = require('path');
const axios = require('axios');

const fetchAndSaveProblems = async () => {
  try {
    const response = await axios.get('http://localhost:8000/fetch_Questions');
    const problemsData = response.data;

    // Define the path to the JSON file in the public folder
    const filePath = path.join(__dirname, '../public/json/questions.json');

    // Write the data to the file
    fs.writeFileSync(filePath, JSON.stringify(problemsData, null, 2));
    console.log('Problems data saved to questions.json');
  } catch (error) {
    console.error('Error fetching or saving problems data:', error);
  }
};

fetchAndSaveProblems();
