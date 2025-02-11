import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# Load environment variables
load_dotenv()

app = Flask(__name__)

def format_phone_number(phone):
    """Format phone number nicely"""
    if phone.startswith('+44'):
        # Convert +44 7xxx xxx xxx to 07xxx xxx xxx
        number = '0' + phone[3:]
        return f"{number[:5]} {number[5:8]} {number[8:]}"
    return phone

def get_html_template(from_number, to_number, message_body, received_at):
    """Generate HTML email template"""
    formatted_from = format_phone_number(from_number)
    formatted_to = format_phone_number(to_number)
    
    # Parse and format the timestamp
    dt = datetime.fromisoformat(received_at.replace('Z', '+00:00'))
    formatted_time = dt.strftime('%d %B %Y at %H:%M:%S')
    
    return f"""
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body style="font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f0f0f0;">
        <div style="max-width: 600px; margin: 0 auto; background-color: white; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            <div style="background-color: #f8f9fa; padding: 25px; border-bottom: 1px solid #dee2e6;">
                <h2 style="color: #333; margin: 0 0 10px 0; font-size: 24px;">New SMS Message Received</h2>
                <p style="color: #666; margin: 0; font-size: 16px;">SMS to Email Notification</p>
            </div>
            
            <div style="padding: 25px;">
                <table style="width: 100%; border-collapse: separate; border-spacing: 0 10px;">
                    <tr>
                        <td style="color: #666; padding-right: 15px; width: 80px; vertical-align: top;">From:</td>
                        <td style="color: #333; font-weight: bold; word-break: break-word;">{formatted_from}</td>
                    </tr>
                    <tr>
                        <td style="color: #666; padding-right: 15px; width: 80px; vertical-align: top;">To:</td>
                        <td style="color: #333; font-weight: bold; word-break: break-word;">{formatted_to}</td>
                    </tr>
                    <tr>
                        <td style="color: #666; padding-right: 15px; width: 80px; vertical-align: top;">Received:</td>
                        <td style="color: #333; font-weight: bold; word-break: break-word;">{formatted_time}</td>
                    </tr>
                </table>
            </div>
            
            <div style="padding: 0 25px 25px 25px;">
                <div style="background-color: #f8f9fa; padding: 25px; border-radius: 6px;">
                    <h3 style="color: #333; margin: 0 0 15px 0; font-size: 18px;">Message Content:</h3>
                    <div style="background-color: white; padding: 25px; border-radius: 4px; border: 1px solid #dee2e6; min-height: 100px;">
                        <p style="white-space: pre-wrap; margin: 0; color: #333; font-size: 16px; line-height: 1.6; word-break: break-word; overflow-wrap: break-word;">{message_body}</p>
                    </div>
                </div>
            </div>
            
            <div style="text-align: center; padding: 25px; background-color: #f8f9fa; border-top: 1px solid #dee2e6;">
                <div style="background-color: #fff3cd; border: 1px solid #ffeeba; color: #856404; padding: 12px 20px; border-radius: 4px; font-size: 14px; text-align: center;">
                    ⚠️ Do not reply to this email. It will not be delivered to the sender.
                </div>
            </div>
        </div>
    </body>
    </html>
    """

def send_email(from_number, message_body, to_number, received_at):
    """Send email using SMTP"""
    msg = MIMEMultipart('alternative')
    msg['From'] = os.getenv('SENDER_EMAIL')
    msg['To'] = os.getenv('RECIPIENT_EMAIL')
    msg['Subject'] = f'SMS from {format_phone_number(from_number)}'
    
    # Create HTML version of the message
    html_content = get_html_template(from_number, to_number, message_body, received_at)
    msg.attach(MIMEText(html_content, 'html'))
    
    try:
        with smtplib.SMTP(os.getenv('SMTP_SERVER'), int(os.getenv('SMTP_PORT'))) as server:
            if os.getenv('SMTP_USE_TLS', 'True').lower() == 'true':
                server.starttls()
            
            server.login(os.getenv('SMTP_USERNAME'), os.getenv('SMTP_PASSWORD'))
            server.send_message(msg)
            
        print(f"Email sent successfully to {os.getenv('RECIPIENT_EMAIL')}")
        return True
    except Exception as e:
        print(f"Failed to send email: {str(e)}")
        return False

@app.route('/webhook', methods=['POST'])
def webhook():
    """Handle incoming SMS webhooks"""
    try:
        # Get the webhook data
        data = request.json
        print("Received webhook data:", data)
        
        # Check if this is a message received event
        if data.get('data', {}).get('event_type') == 'message.received':
            payload = data['data']['payload']
            from_number = payload['from']['phone_number']
            to_number = payload['to'][0]['phone_number']
            message_body = payload['text']
            received_at = payload['received_at']
            
            # Send email with all parameters
            if send_email(from_number, message_body, to_number, received_at):
                return jsonify({'status': 'success', 'message': 'Email sent'}), 200
            else:
                return jsonify({'status': 'error', 'message': 'Failed to send email'}), 500
        
        return jsonify({'status': 'ignored', 'message': 'Not a message.received event'}), 200
        
    except Exception as e:
        print(f"Error processing webhook: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    print("Starting SMS to Email forwarder...")
    print(f"Will forward messages to {os.getenv('RECIPIENT_EMAIL')}")
    print("\nListening for webhooks on port 5000")
    print("Configure your SMS provider to send webhooks to:")
    print("http://YOUR_SERVER_IP:5000/webhook")
    app.run(host='0.0.0.0', port=5000)
