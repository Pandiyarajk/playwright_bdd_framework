"""
Microsoft Teams Webhook Integration.
Send instant alerts to Microsoft Teams for test case status and duration.
"""

import pymsteams
from typing import Optional, Dict, Any
from powerlogger import get_logger

logger = get_logger(__name__)


class TeamsWebhook:
    """
    Microsoft Teams webhook integration for sending test alerts.
    
    Usage:
        webhook = TeamsWebhook("https://your-company.webhook.office.com/webhookb2/your-webhook-url")
        
        result = webhook.send_message(
            message_title="🚨 Alert",
            activity_title="System Monitor",
            activity_subtitle="Health Check",
            text_message="This is a test message!"
        )
    """
    
    def __init__(self, webhook_url: str):
        """
        Initialize Teams webhook.
        
        Args:
            webhook_url: Microsoft Teams incoming webhook URL
        """
        self.webhook_url = webhook_url
        logger.info(f"🔗 Teams webhook initialized")
    
    def send_message(
        self,
        message_title: str,
        activity_title: Optional[str] = None,
        activity_subtitle: Optional[str] = None,
        text_message: Optional[str] = None,
        color: Optional[str] = None,
        facts: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Send a message to Microsoft Teams channel.
        
        Args:
            message_title: Main title of the message
            activity_title: Activity section title
            activity_subtitle: Activity section subtitle
            text_message: Main text content
            color: Theme color (hex color code, e.g., '#FF0000' for red)
            facts: Dictionary of key-value pairs to display as facts
            
        Returns:
            Dictionary with 'success' boolean and optional 'error' message
        """
        try:
            # Create connector card
            card = pymsteams.connectorcard(self.webhook_url)
            
            # Set title
            card.title(message_title)
            
            # Set main text if provided
            if text_message:
                card.text(text_message)
            
            # Set color theme if provided
            if color:
                card.color(color)
            
            # Add activity section if provided
            if activity_title or activity_subtitle:
                card.addLinkButton("View Details", "#")  # Placeholder for potential link
            
            # Create a section for additional details
            if activity_title or activity_subtitle or facts:
                section = pymsteams.cardsection()
                
                if activity_title:
                    section.activityTitle(activity_title)
                
                if activity_subtitle:
                    section.activitySubtitle(activity_subtitle)
                
                # Add facts if provided
                if facts:
                    for name, value in facts.items():
                        section.addFact(name, value)
                
                card.addSection(section)
            
            # Send the message
            card.send()
            
            logger.info(f"✅ Teams message sent successfully: {message_title}")
            return {"success": True}
            
        except Exception as e:
            error_msg = f"Failed to send Teams message: {str(e)}"
            logger.error(f"❌ {error_msg}")
            return {"success": False, "error": error_msg}
    
    def send_test_alert(
        self,
        test_name: str,
        status: str,
        duration: float,
        test_case_id: Optional[str] = None,
        feature_name: Optional[str] = None,
        error_message: Optional[str] = None,
        tags: Optional[list] = None
    ) -> Dict[str, Any]:
        """
        Send a test case status alert to Teams.
        
        Args:
            test_name: Name of the test/scenario
            status: Test status (passed, failed, skipped)
            duration: Test execution duration in seconds
            test_case_id: Test case identifier
            feature_name: Feature name
            error_message: Error message if test failed
            tags: List of test tags
            
        Returns:
            Dictionary with 'success' boolean and optional 'error' message
        """
        # Determine emoji and color based on status
        status_config = {
            'passed': {'emoji': '✅', 'color': '#28a745', 'title': 'Test Passed'},
            'failed': {'emoji': '❌', 'color': '#dc3545', 'title': 'Test Failed'},
            'skipped': {'emoji': '⏭️', 'color': '#ffc107', 'title': 'Test Skipped'}
        }
        
        config = status_config.get(status.lower(), status_config['failed'])
        
        # Build message title
        message_title = f"{config['emoji']} {config['title']}: {test_name}"
        
        # Build facts dictionary
        facts = {
            "Status": status.upper(),
            "Duration": f"{duration:.2f}s"
        }
        
        if test_case_id:
            facts["Test Case ID"] = test_case_id
        
        if feature_name:
            facts["Feature"] = feature_name
        
        if tags:
            facts["Tags"] = ", ".join(tags)
        
        # Build text message
        text_parts = [f"Test execution completed with status: **{status.upper()}**"]
        
        if error_message:
            text_parts.append(f"\n\n**Error:**\n```\n{error_message}\n```")
        
        text_message = "\n".join(text_parts)
        
        # Send the message
        return self.send_message(
            message_title=message_title,
            activity_title="Test Automation Alert",
            activity_subtitle=test_case_id or test_name,
            text_message=text_message,
            color=config['color'],
            facts=facts
        )
    
    def send_summary_alert(
        self,
        total: int,
        passed: int,
        failed: int,
        skipped: int,
        duration: float,
        pass_rate: float
    ) -> Dict[str, Any]:
        """
        Send a test execution summary alert to Teams.
        
        Args:
            total: Total number of tests
            passed: Number of passed tests
            failed: Number of failed tests
            skipped: Number of skipped tests
            duration: Total execution duration in seconds
            pass_rate: Pass rate percentage
            
        Returns:
            Dictionary with 'success' boolean and optional 'error' message
        """
        # Determine overall status
        if failed > 0:
            emoji = '❌'
            status_text = 'FAILED'
            color = '#dc3545'
        elif passed == total:
            emoji = '✅'
            status_text = 'PASSED'
            color = '#28a745'
        else:
            emoji = '⚠️'
            status_text = 'PARTIAL'
            color = '#ffc107'
        
        message_title = f"{emoji} Test Execution {status_text}"
        
        # Build facts
        facts = {
            "Total Tests": str(total),
            "✅ Passed": str(passed),
            "❌ Failed": str(failed),
            "⏭️ Skipped": str(skipped),
            "Pass Rate": f"{pass_rate:.1f}%",
            "Duration": f"{duration:.2f}s"
        }
        
        text_message = f"Test automation execution completed.\n\n**Overall Status:** {status_text}"
        
        return self.send_message(
            message_title=message_title,
            activity_title="Test Execution Summary",
            activity_subtitle=f"Executed {total} test scenarios",
            text_message=text_message,
            color=color,
            facts=facts
        )


def create_teams_webhook(config_manager) -> Optional[TeamsWebhook]:
    """
    Factory function to create Teams webhook from config.
    
    Args:
        config_manager: ConfigManager instance
        
    Returns:
        TeamsWebhook instance or None if not enabled
    """
    enabled = config_manager.get('teams', 'enabled', False)
    
    if not enabled:
        return None
    
    webhook_url = config_manager.get('teams', 'webhook_url', '')
    
    if not webhook_url or webhook_url == 'https://your-company.webhook.office.com/webhookb2/your-webhook-url':
        logger.warning("⚠️ Teams webhook URL not configured")
        return None
    
    try:
        return TeamsWebhook(webhook_url)
    except Exception as e:
        logger.error(f"❌ Failed to create Teams webhook: {e}")
        return None
