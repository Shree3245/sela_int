# Voice AI Assistant with Twilio and OpenAI

This project implements a voice-based AI assistant using Twilio for voice handling and OpenAI's GPT for conversation. Users can call a Twilio number and have an interactive conversation with an AI.

## Prerequisites

- Python 3.8+
- A Twilio account with:
  - Account SID
  - Auth Token
  - Phone Number
- An OpenAI API key
- ngrok for local development

## Getting Your API Keys

### Twilio Setup
1. Sign up for a [Twilio account](https://www.twilio.com/try-twilio)
2. Once logged in, find your Account SID and Auth Token on the [Twilio Console Dashboard](https://console.twilio.com/)
3. Get a Twilio phone number:
   - Go to [Phone Numbers](https://console.twilio.com/us1/develop/phone-numbers/manage/incoming) in your Twilio Console
   - Click "Buy a number" or "Get a trial number"
   - Make sure the number has voice capabilities

### OpenAI Setup
1. Create an account on [OpenAI](https://platform.openai.com/signup)
2. Go to [API Keys](https://platform.openai.com/account/api-keys)
3. Click "Create new secret key"
4. Copy your API key immediately (it won't be shown again)

## Installation

1. Clone the repository
2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file with the following variables:
   - `TWILLIO_ACCOUNT_SID_LIVE`
   - `TWILLIO_AUTH_TOKEN_LIVE`
   - `OPENAI_API_KEY`

## Running the Application

1. Start ngrok:
   ```bash
   ngrok http http://localhost:8000
   ```
2. Run the FastAPI application:
   ```bash
   uvicorn app:app --port 8000
   ```

3. Make sure your ngrok URL is set in the Twilio webhook settings.

4. Call the Twilio number and start interacting with your AI assistant!
