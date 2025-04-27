import { Router, Request, Response } from 'express';
import path from 'path';
import fs from 'fs';

const router = Router();

// Home page
router.get('/', (req: Request, res: Response) => {
  res.sendFile(path.join(__dirname, '../public/index.html'));
});

// Dashboard page
router.get('/dashboard', (req: Request, res: Response) => {
  res.sendFile(path.join(__dirname, '../public/dashboard.html'));
});

// Trials page
router.get('/trials', (req: Request, res: Response) => {
  res.sendFile(path.join(__dirname, '../public/trials.html'));
});

// Payments page
router.get('/payments', (req: Request, res: Response) => {
  res.sendFile(path.join(__dirname, '../public/payments.html'));
});

// Referrals page
router.get('/referrals', (req: Request, res: Response) => {
  res.sendFile(path.join(__dirname, '../public/referrals.html'));
});

// Bot control page (admin only)
router.get('/admin/bot', (req: Request, res: Response) => {
  res.sendFile(path.join(__dirname, '../public/admin/bot.html'));
});

export default router;