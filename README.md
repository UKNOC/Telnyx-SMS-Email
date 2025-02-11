# SMS to Email Forwarder

A simple yet powerful Flask application that forwards SMS messages to your email inbox. Originally developed for radio stations to receive SMS messages from listeners, this application has been made available to the wider community for various use cases.

## Features

- **SMS to Email Forwarding**: Automatically converts incoming SMS messages into beautifully formatted HTML emails
- **UK Phone Number Formatting**: Intelligently formats UK phone numbers (e.g., converts +447xxx xxx xxx to 07xxx xxx xxx)
- **Modern Email Template**: Clean, responsive HTML email design that looks great on all devices
- **Health Monitoring**: Built-in health check endpoint for monitoring application status
- **Secure**: Supports TLS for SMTP connections
- **Easy Setup**: Simple configuration using environment variables

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

Configure your SMS provider to send webhooks to:
```
http://YOUR_SERVER_IP:5000/webhook
```

The application expects webhooks in the following format:
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

Monitor your application's health by making a GET request to:
```
http://YOUR_SERVER_IP:5000/health
```

A successful response will return:
```json
{
  "status": "healthy"
}
```

## Production Deployment

For production deployment:

1. Use HTTPS for your webhook endpoint
2. Run behind a reverse proxy (e.g., Nginx)
3. Consider implementing webhook authentication
4. Use environment variables for sensitive configuration
5. Monitor the health check endpoint

## Background

This application was originally developed for radio stations to receive SMS messages from listeners. The stations needed a simple way to receive and archive text messages without relying on physical phones or complex systems. We've now made it available to the wider community as it can be useful for many other scenarios:

- Customer service message monitoring
- SMS alerts and notifications
- Personal SMS archiving
- Business SMS management

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
