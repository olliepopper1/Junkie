"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const express_1 = __importDefault(require("express"));
const cors_1 = __importDefault(require("cors"));
const path_1 = __importDefault(require("path"));
const bot_1 = __importDefault(require("./routes/bot"));
const api_1 = __importDefault(require("./routes/api"));
const web_1 = __importDefault(require("./routes/web"));
// Create Express server
const app = (0, express_1.default)();
const port = process.env.PORT || 5000;
// Express configuration
app.use((0, cors_1.default)());
app.use(express_1.default.json());
app.use(express_1.default.urlencoded({ extended: true }));
app.use(express_1.default.static(path_1.default.join(__dirname, 'public')));
// Set view engine
app.set('views', path_1.default.join(__dirname, 'views'));
app.set('view engine', 'html');
app.engine('html', (filePath, options, callback) => {
    // Simple HTML file serving
    require('fs').readFile(filePath, 'utf-8', callback);
});
// Routes
app.use('/bot', bot_1.default);
app.use('/api', api_1.default);
app.use('/', web_1.default);
// Start the server
app.listen(port, () => {
    console.log(`Server running on port ${port}`);
});
//# sourceMappingURL=index.js.map