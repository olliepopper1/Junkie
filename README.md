# Trial Junkie

A sophisticated multi-agent automation platform specializing in dynamic trial generation and management with intelligent service integrations.

## Overview

This system automates real free trial signups using only the provided RapidAPI Hub APIs. It uses:

- Real-time email + phone validation
- Realistic credit card data to pass trial system
- Real-time person verification
- Full web automation to submit trials
- Discord bot control and notifications

## Required Environment Variables

Add these in Replit Secrets tab:

- `RAPIDAPI_KEY`: Your RapidAPI key for accessing all APIs
- `DISCORD_BOT_TOKEN`: Your Discord bot token for the control bot
- `ADMIN_USERNAME`: Username for admin access
- `ADMIN_PASSWORD`: Password for admin access
- `WALLET_SECRET_KEY`: Solana wallet secret key

## Connected APIs (Through RapidAPI Hub)

1. **Abstract Phone Number Validation**
   - Validates: Number format, country, line type
   - Endpoint: `https://phonevalidation.abstractapi.com/v1/?api_key=RAPIDAPI_KEY&phone=+1234567890`

2. **Veriphone**
   - Validates: Phone number globally (carrier, format, validity)
   - Endpoint: `https://veriphone.p.rapidapi.com/verify?phone=+1234567890`

3. **Personator by Melissa Data**
   - Verifies: Full contact info — name, email, phone, address
   - Endpoint: `https://personator.melissadata.net/v3/WEB/ContactVerify/doContactVerify`

4. **ScrapeNinja**
   - Scrapes/Accesses: Hulu pages for rendering, bypassing protection
   - Endpoint: `https://scrapeninja.p.rapidapi.com/scrape`

5. **Fake Valid CC Data Generator**
   - Generates: Realistic-looking valid credit card data
   - Endpoint: `https://fake-valid-cc-data-generator.p.rapidapi.com/generate?brand=visa&format=json`

6. **Advanced Email Validator**
   - Validates: Structure, MX records, SMTP server, domain
   - Endpoint: `https://advanced-email-validator.p.rapidapi.com/validate`

7. **Fast & Reliable Disposable Email Checker**
   - Checks: If an email is temporary/disposable
   - Endpoint: `https://disposable-email-checker.p.rapidapi.com/?email=test@example.com`

## Core Components

### RapidAPI Integration (`updated_api_integrations.py`)
Connects to all required APIs and provides centralized access to their functionality.

### Hulu Trial Generator (`hulu_trial_generator.py`)
Creates real Hulu trials by:
1. Generating identity with Personator API
2. Validating phone with Veriphone API
3. Creating a valid credit card with the Fake Valid CC Data Generator
4. Automating the trial signup process

### Discord Bot (`updated_discord_bot.py`)
Provides a user-friendly interface for:
1. Trial generation
2. Account management
3. Admin controls
4. One-time trial limit enforcement

## Usage

### Running the Discord Bot

```bash
# Make the run script executable
chmod +x run_trial_junkie_bot.sh

# Run the bot
./run_trial_junkie_bot.sh
```

### Discord Bot Commands

- `/hit [service]` - Generate a complete trial (e.g., `/hit hulu`)
- `/stash` - View your saved trials
- `/rehab` - Clear your saved data
- `/quote [agent]` - Get a quote from an agent
- `/agents` - View all available agents
- `/admin login [username] [password]` - Admin login
- `/admin reset [user_id]` - Reset a user's trial limit

### Admin Functions

Admin users can:
1. Log in using the provided credentials
2. Reset user trial limits to allow additional trials
3. Override the one-time trial restriction

## System Architecture

1. **API Integration Layer**: Connects to RapidAPI Hub services
2. **Data Generation Layer**: Creates realistic information for trial signups
3. **Automation Layer**: Handles browser automation for websites
4. **Bot Control Layer**: Manages Discord commands and user interaction
5. **Security Layer**: Ensures one-time usage and admin controls

## Future Enhancements

- Add support for additional services (Disney+, Spotify, YouTube Premium)
- Implement expanded automation capabilities
- Add wallet integration for payment handling
- Create a web interface for the service