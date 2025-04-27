import express from 'express';
import cors from 'cors';
import path from 'path';
import botRouter from './routes/bot';
import apiRouter from './routes/api';
import webRouter from './routes/web';

// Create Express server
const app = express();
const port = process.env.PORT || 5000;

// Express configuration
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, 'public')));

// Set view engine
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'html');
app.engine('html', (filePath, options, callback) => {
  // Simple HTML file serving
  require('fs').readFile(filePath, 'utf-8', callback);
});

// Routes
app.use('/bot', botRouter);
app.use('/api', apiRouter);
app.use('/', webRouter);

// Start the server
app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});