# Telnyx SMS to Email Forwarder

A Flask application that forwards SMS messages from Telnyx to your email inbox. Originally developed for radio stations to receive SMS messages from listeners, this application has been made available to the wider community.

## Features

- Forward SMS messages to email with a clean HTML template
- Format UK phone numbers (converts +447xxx xxx xxx to 07xxx xxx xxx)
- Health check endpoint for monitoring
- TLS support for secure SMTP connections
- Simple configuration using environment variables

## Quick Start

1. Clone this repository:
   ```bash
   git clone https://github.com/UKNOC/Telnyx-SMS-Email.git
   cd Telnyx-SMS-Email
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Copy the example environment file and configure your settings:
   ```bash
   cp .env.example .env
   ```

4. Edit `.env` with your SMTP and email settings:
   ```
   SMTP_SERVER=smtp.example.com
   SMTP_PORT=587
   SMTP_USERNAME=your_username
   SMTP_PASSWORD=your_password
   SMTP_USE_TLS=True
   
   SENDER_EMAIL=sms-notifications@yourdomain.com
   RECIPIENT_EMAIL=your-email@yourdomain.com
   ```

5. Start the application:
   ```bash
   python app.py
   ```

## Webhook Configuration

Configure your Telnyx number to send webhooks to:
```
http://YOUR_SERVER_IP:5000/webhook
```

The application expects webhooks in this format:
```json
{
  "data": {
    "event_type": "message.received",
    "payload": {
      "from": {
        "phone_number": "+447123456789"
      },
      "to": [{
        "phone_number": "+447987654321"
      }],
      "text": "Hello, this is a test message!",
      "received_at": "2025-02-11T19:09:39Z"
    }
  }
}
```

## Health Check

Monitor the application's health:
```
http://YOUR_SERVER_IP:5000/health
```

Response:
```json
{
  "status": "healthy"
}
```

## Production Deployment

For production:

1. Use HTTPS for your webhook endpoint
2. Run behind a reverse proxy (e.g., Nginx)
3. Consider implementing webhook authentication
4. Use environment variables for sensitive configuration
5. Monitor the health check endpoint

## Background

This application was developed for radio stations needing a simple way to receive SMS messages from listeners without physical phones. It's now available for other use cases like:

- Customer service monitoring
- SMS alerts and notifications
- Personal message archiving
- Business SMS management

## Contributing

Contributions are welcome. Please submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
