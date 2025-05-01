import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import current_app, render_template
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def send_email(recipient, subject, template, **kwargs):
    """
    Send an email using the configured SMTP server.
    
    Args:
        recipient (str): Recipient email address
        subject (str): Email subject
        template (str): Name of the HTML template to use
        **kwargs: Template variables
    
    Returns:
        dict: {'success': bool, 'message': str}
    """
    try:
        # Get SMTP configuration from app config
        smtp_host = current_app.config['SMTP_HOST']
        smtp_port = current_app.config['SMTP_PORT']
        smtp_user = current_app.config['SMTP_USER']
        smtp_pass = current_app.config['SMTP_PASS']
        from_email = current_app.config['SMTP_FROM_EMAIL']
        
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = from_email
        msg['To'] = recipient
        
        # Create the HTML content (normally would render a template)
        # Since we haven't implemented templates yet, we'll use a simple HTML message
        html_content = f"<html><body><h2>{subject}</h2><p>{kwargs.get('message', '')}</p></body></html>"
        
        # Attach HTML content
        msg.attach(MIMEText(html_content, 'html'))
        
        # Send email
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.send_message(msg)
        
        logger.info(f"Email sent to {recipient} with subject: {subject}")
        return {
            'success': True,
            'message': 'Email sent successfully'
        }
    
    except Exception as e:
        logger.error(f"Error sending email: {str(e)}")
        return {
            'success': False,
            'message': f"Failed to send email: {str(e)}"
        }

def send_team_invitation(recipient_email, team_name, inviter_name):
    """Send an email invitation to join a team"""
    subject = f"Invitation to join team {team_name}"
    message = f"You've been invited by {inviter_name} to join the team '{team_name}' on WisePair."
    
    return send_email(
        recipient=recipient_email,
        subject=subject,
        template='team_invitation.html',  # This would be the template if implemented
        message=message,
        team_name=team_name,
        inviter_name=inviter_name
    )

def send_mentor_request(recipient_email, team_name, message=None):
    """Send an email to a professor/mentor for mentorship request"""
    subject = f"Mentorship Request from team {team_name}"
    email_message = f"Team '{team_name}' has requested your mentorship on WisePair."
    
    if message:
        email_message += f"\n\nMessage from team: {message}"
    
    return send_email(
        recipient=recipient_email,
        subject=subject,
        template='mentor_request.html',  # This would be the template if implemented
        message=email_message,
        team_name=team_name
    )

def send_request_response(recipient_email, team_name, status, responder_name):
    """Send an email about mentor/professor response to request"""
    subject = f"Mentorship Request {status.capitalize()}"
    message = f"Your mentorship request to {responder_name} for team '{team_name}' has been {status}."
    
    return send_email(
        recipient=recipient_email,
        subject=subject,
        template='request_response.html',  # This would be the template if implemented
        message=message,
        team_name=team_name,
        status=status,
        responder_name=responder_name
    )

def send_meeting_notification(recipient_email, meeting_title, team_name, scheduled_date):
    """Send a meeting notification email"""
    subject = f"Meeting Scheduled: {meeting_title}"
    message = f"A meeting '{meeting_title}' has been scheduled for team '{team_name}' on {scheduled_date}."
    
    return send_email(
        recipient=recipient_email,
        subject=subject,
        template='meeting_notification.html',  # This would be the template if implemented
        message=message,
        meeting_title=meeting_title,
        team_name=team_name,
        scheduled_date=scheduled_date
    ) 