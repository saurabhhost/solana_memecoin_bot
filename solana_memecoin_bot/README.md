# Solana Memecoin Trading Bot

A Python-based bot to automate Solana memecoin trading with real-time data analysis, safety checks, and trading execution.

## Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Update `config.json` with your Telegram bot token and chat ID.
3. Run the bot: `./run.sh`

## Features
- Monitors PumpFun and GMGN for trending coins.
- Safety checks via RugCheck.xyz (score >= 85%, liquidity burned, non-mintable, non-pausable).
- Social analysis via TweetScout.io (influencers with 10k+ followers).
- Trades via Toxi Bot with 0.01–0.15 SOL buys, 30% slippage, and 10x profit sell.
