const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const pythonScript = path.join(__dirname, '../backend/run.py');
    const pythonProcess = spawn('python', [pythonScript]);
    
    let stdout = '';
    let stderr = '';

    pythonProcess.stdout.on('data', (data) => {
      stdout += data.toString();
    });

    pythonProcess.stderr.on('data', (data) => {
      stderr += data.toString();
    });

    pythonProcess.on('close', (code) => {
      if (code !== 0) {
        console.error('Python script error:', stderr);
        return res.status(500).json({ error: 'Internal server error' });
      }

      try {
        const result = JSON.parse(stdout);
        res.status(200).json(result);
      } catch (e) {
        res.status(500).json({ error: 'Invalid response' });
      }
    });

  } catch (error) {
    console.error('Error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
}
