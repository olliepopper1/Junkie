# Trial Junkie

A sophisticated multi-agent automation platform with dynamic web interface and Discord bot integration for generating and managing digital service trials with real automation capabilities.

## Overview

Trial Junkie is a complete trial account generation solution that provides both a web application and Discord bot interface. The system creates genuine trial accounts for various streaming and subscription services using advanced browser automation. 

The platform consists of multiple specialized agents, each handling a different aspect of the trial creation process:

- **Identity Agent (Heroin Harry)**: Generates realistic user identities
- **Card Agent (Cash Carter)**: Creates valid credit card information for trial signups
- **Email Agent (Vape Vince)**: Generates email addresses and handles verification
- **Phone Agent (Molly Morphine)**: Provides phone verification services
- **Automation Agent (Keta Kev)**: Handles browser automation and continuous trial generation

## Key Features

- **Dual Interface**: Access via a modern web application or Discord bot
- **Solana Wallet Integration**: Secure authentication and payment processing using Phantom wallet
- **Real Trial Creation**: Automates browser interactions to create actual working trial accounts
- **Modular Agent Architecture**: Each specialized agent handles a different aspect of the process
- **Service Flexibility**: Works with predefined services or any custom trial website URL
- **Subscription Tiers**: Multiple membership levels with different access and usage limits
- **Database Integration**: Stores user credentials and trial information securely
- **Referral System**: Users can earn commissions by referring others

## Discord Commands

- `!hit <service>` - Generate a complete trial for a service (all agents)
- `!dose <agent> <service>` - Generate a specific resource (single agent)
- `!trip <script>` - Run automation scripts for predefined services
- `!stash` - View your generated credentials
- `!rehab` - Clear your data
- `!quote <agent>` - Get a random quote from an agent
- `!agents` - See information about all agents
- `!plans` - View subscription plans
- `!pay <service_type>` - Payment command
- `!tier` - View your subscription tier

## Installation and Setup

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Set up environment variables in `.env`:
   ```
   # Discord Bot
   DISCORD_BOT_TOKEN=your_discord_bot_token
   
   # Database
   DATABASE_URL=your_database_url
   
   # Solana Wallet
   SOLANA_WALLET_ADDRESS=your_solana_wallet
   SOLANA_NETWORK=devnet  # or mainnet-beta for production
   
   # External APIs
   RAPIDAPI_KEY=your_rapidapi_key
   
   # Session security
   SESSION_SECRET=your_session_secret
   ```

4. Run the web application:
   ```
   gunicorn --bind 0.0.0.0:5000 --reuse-port --reload main:app
   ```

5. Run the Discord bot (separate process):
   ```
   python discord_bot.py
   ```

### Solana Wallet Setup

To receive payments through the application:

1. Create a Solana wallet using [Phantom](https://phantom.app/)
2. Set your wallet address in the `.env` file as `SOLANA_WALLET_ADDRESS`
3. For testing, use Solana devnet
4. For production, switch to mainnet-beta and ensure proper key management

## Real Trial Automation

The system uses Selenium with ChromeDriver to automate the trial creation process. This involves:

1. Generating realistic user information (name, address, email, etc.)
2. Creating valid credit card information
3. Navigating to the service's website
4. Filling out registration forms
5. Handling payment verification
6. Creating a working trial account

### Supported Services

The following services have specialized automation scripts:

- Hulu
- Netflix
- Disney+
- YouTube Premium
- Spotify
- Amazon Prime
- Paramount+
- HBO Max
- Peacock

Additionally, the system can attempt to automate trial creation on any website URL using the generic automation functionality.

## Testing

The project includes a comprehensive test suite covering all major components:

### API Tests

These tests verify all API endpoints are functioning correctly:

```
python test_api_endpoints.py
```

Tests cover:
- Authentication flows (registration, login, wallet connection)
- Trial generation endpoints
- Payment processing
- Referral system functionality

### Payment Flow Tests

Tests for the Solana wallet payment integration:

```
python test_payment_flow.py
```

Tests cover:
- Wallet connection
- Payment creation and verification
- Subscription activation and expiration
- Error handling

### Discord Bot Tests

Test Discord bot commands and functionality:

```
python test_discord_commands.py
```

Tests cover:
- Command availability and responses
- Error handling
- User permission checks
- Integration with the database

### Trial Automation Tests

Test the browser automation for specific services:

```
python test_hulu_trial.py
```

This runs a comprehensive test of the Hulu trial creation process, including identity generation, card creation, and browser automation.

### API Integration Tests

Test external API integrations for identity and card generation:

```
python test_api_integrations.py
```

### Manual Testing

To simulate a complete user flow through the Discord bot:

```
python simulate_hit_command.py
```

This simulates what happens when a user runs the `!hit hulu` command in Discord.

## Technical Details

### Architecture

- **Backend**: Flask-based Python application with RESTful API endpoints
- **Frontend**: Responsive design built with modern HTML/CSS/JavaScript and character-driven UI
- **Database**: SQLite for development, PostgreSQL for production with SQLAlchemy ORM
- **Authentication**: Dual system with Solana wallet integration and traditional email/password

### Key Components

- **Browser Automation**: Selenium with ChromeDriver for website interaction
- **Payment System**: Integrated with Solana blockchain for secure and decentralized payments
- **API Integration**: Uses RapidAPI services for identity, phone verification, and card generation
- **Discord Integration**: Seamless connection between web app and Discord bot functionality

### Security

- **Wallet Authentication**: Non-custodial wallet-based login with Phantom
- **Encrypted Storage**: Sensitive user data and credentials are encrypted at rest
- **Session Management**: Secure session handling with proper expiration and renewal
- **Access Control**: Role-based permissions with subscription tier enforcement

## Responsible Usage

This tool is intended for educational purposes and legitimate trial usage. Please:

1. Use real information when signing up for trials
2. Remember to cancel trials before they convert to paid subscriptions
3. Respect the terms of service of the websites you interact with

## Contributing

Contributions are welcome! Please feel free to submit a pull request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.