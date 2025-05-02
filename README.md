# Trial Junkie

A sophisticated multi-agent automation platform specializing in dynamic trial generation and management with intelligent service integrations and Discord bot capabilities.

## Overview

Trial Junkie automates the creation of legitimate free trial accounts for various streaming services using RapidAPI Hub APIs for identity generation, phone verification, credit card validation, and more. The system features a Discord bot interface for easy user interaction and a comprehensive backend for managing trials.

## Core Components

- **API Integrations**: Connects to external APIs for identity generation, card validation, and more
- **Trial Generation**: Creates actual trials using the provided APIs with robust fallback mechanisms
- **Database Storage**: Stores user information and trial data securely
- **Discord Bot**: Provides a user-friendly interface via Discord commands
- **Trial Delivery**: Delivers trial information to users via Discord DMs

## Setup

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up environment variables (see `.env.example`)
4. Run the setup script: `python setup_trialjunkie.py`
5. Start the Discord bot: `python run_discord_integration.py`

## Environment Variables

Create a `.env` file with the following variables:

```
# Database
DATABASE_URL=postgresql://username:password@localhost:5432/database_name

# Discord Bot
DISCORD_BOT_TOKEN=your_discord_bot_token

# API Keys
RAPIDAPI_KEY=your_rapidapi_key
```

## Commands

The Discord bot supports the following commands:

- `!hit <service>`: Generate a trial for a specific service (e.g., `!hit hulu`)
- `!stash`: View your generated trials
- `!helpme`: Display help information

## Supported Services

- Hulu
- Netflix
- Disney+
- Spotify
- Apple Music
- YouTube Premium
- HBO Max

## Architecture

The system is built with a modular architecture:

1. **trial_junkie_system.py**: Core system that integrates all components
2. **updated_api_integrations.py**: Handles all external API calls with fallback mechanisms
3. **database.py**: Manages database connections and operations
4. **bot_trial_delivery.py**: Delivers trials to users
5. **integrated_discord_bot.py**: Provides the Discord bot interface
6. **setup_trialjunkie.py**: Initializes and tests the system

## Fallback Mechanisms

The system includes multi-level fallback mechanisms for all API functions:

1. **Primary API**: Attempts to use the configured RapidAPI endpoints
2. **Secondary API**: Falls back to alternative API endpoints if primary fails
3. **Cached Data**: Uses previously cached successful responses when available
4. **Local Generation**: Uses algorithmic generation as a final fallback option

## Limitations

- Some services may require additional verification steps
- Trial availability depends on the service's policies
- API rate limits may affect generation speed and success rate

## Development

To contribute to the project:

1. Fork the repository
2. Create a feature branch
3. Make changes and add tests
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.