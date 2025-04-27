"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const express_1 = require("express");
const path_1 = __importDefault(require("path"));
const router = (0, express_1.Router)();
// Home page
router.get('/', (req, res) => {
    res.sendFile(path_1.default.join(__dirname, '../public/index.html'));
});
// Dashboard page
router.get('/dashboard', (req, res) => {
    res.sendFile(path_1.default.join(__dirname, '../public/dashboard.html'));
});
// Trials page
router.get('/trials', (req, res) => {
    res.sendFile(path_1.default.join(__dirname, '../public/trials.html'));
});
// Payments page
router.get('/payments', (req, res) => {
    res.sendFile(path_1.default.join(__dirname, '../public/payments.html'));
});
// Referrals page
router.get('/referrals', (req, res) => {
    res.sendFile(path_1.default.join(__dirname, '../public/referrals.html'));
});
// Bot control page (admin only)
router.get('/admin/bot', (req, res) => {
    res.sendFile(path_1.default.join(__dirname, '../public/admin/bot.html'));
});
exports.default = router;
//# sourceMappingURL=web.js.map