"""Email reporting functionality."""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
import logging


class EmailReporter:
    """Send email reports for test execution."""
    
    def __init__(self, config_manager):
        """
        Initialize email reporter.
        
        Args:
            config_manager: Configuration manager instance
        """
        self.config = config_manager
        self.logger = logging.getLogger('AutomationFramework.EmailReporter')
        
        # Get email configuration
        self.smtp_server = config_manager.get('email', 'smtp_server', 'smtp.gmail.com')
        self.smtp_port = config_manager.get('email', 'smtp_port', 587)
        self.use_tls = config_manager.get('email', 'use_tls', True)
        self.from_email = config_manager.get('email', 'from_email', '')
        self.to_emails = config_manager.get('email', 'to_emails', '').split(',')
        self.to_emails = [email.strip() for email in self.to_emails if email.strip()]
        self.subject_prefix = config_manager.get('email', 'subject_prefix', '[Test Automation]')
        
        # Get credentials from environment if not in config
        import os
        self.smtp_username = os.getenv('SMTP_USERNAME', self.from_email)
        self.smtp_password = os.getenv('SMTP_PASSWORD', '')
    
    def send_email(
        self,
        subject: str,
        body: str,
        attachments: Optional[List[str]] = None,
        html: bool = True
    ) -> bool:
        """
        Send email.
        
        Args:
            subject: Email subject
            body: Email body
            attachments: List of file paths to attach
            html: Whether body is HTML
            
        Returns:
            True if email sent successfully
        """
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.from_email
            msg['To'] = ', '.join(self.to_emails)
            msg['Subject'] = f"{self.subject_prefix} {subject}"
            
            # Add body
            if html:
                msg.attach(MIMEText(body, 'html'))
            else:
                msg.attach(MIMEText(body, 'plain'))
            
            # Add attachments
            if attachments:
                for file_path in attachments:
                    if Path(file_path).exists():
                        with open(file_path, 'rb') as f:
                            part = MIMEBase('application', 'octet-stream')
                            part.set_payload(f.read())
                            encoders.encode_base64(part)
                            part.add_header(
                                'Content-Disposition',
                                f'attachment; filename= {Path(file_path).name}'
                            )
                            msg.attach(part)
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                if self.use_tls:
                    server.starttls()
                
                if self.smtp_username and self.smtp_password:
                    server.login(self.smtp_username, self.smtp_password)
                
                server.send_message(msg)
            
            self.logger.info(f"Email sent to {', '.join(self.to_emails)}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to send email: {e}")
            return False
    
    def send_summary_report(self, test_results: Dict) -> bool:
        """
        Send test execution summary report.
        
        Args:
            test_results: Test results dictionary
            
        Returns:
            True if email sent successfully
        """
        # Determine status
        total = test_results.get('total', 0)
        passed = test_results.get('passed', 0)
        failed = test_results.get('failed', 0)
        
        if failed > 0:
            status = 'FAILED'
            status_color = '#dc3545'
        elif passed == total:
            status = 'PASSED'
            status_color = '#28a745'
        else:
            status = 'PARTIAL'
            status_color = '#ffc107'
        
        # Calculate pass rate
        pass_rate = (passed / total * 100) if total > 0 else 0
        
        # Create subject
        subject = f"Test Execution {status} - {passed}/{total} Passed"
        
        # Create HTML body
        body = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .header {{ background-color: {status_color}; color: white; padding: 20px; border-radius: 5px; }}
                .summary {{ margin: 20px 0; padding: 15px; background-color: #f8f9fa; border-radius: 5px; }}
                .metrics {{ display: flex; justify-content: space-around; margin: 20px 0; }}
                .metric {{ text-align: center; padding: 15px; background-color: white; border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
                .metric-value {{ font-size: 36px; font-weight: bold; }}
                .metric-label {{ color: #6c757d; margin-top: 5px; }}
                .scenarios {{ margin: 20px 0; }}
                .scenario {{ padding: 10px; margin: 5px 0; border-left: 4px solid #dee2e6; background-color: #f8f9fa; }}
                .scenario.passed {{ border-left-color: #28a745; }}
                .scenario.failed {{ border-left-color: #dc3545; }}
                .footer {{ margin-top: 30px; padding-top: 20px; border-top: 1px solid #dee2e6; color: #6c757d; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Test Execution Report</h1>
                <p>Status: {status}</p>
            </div>
            
            <div class="summary">
                <h2>Execution Summary</h2>
                <p><strong>Start Time:</strong> {test_results.get('start_time', 'N/A')}</p>
                <p><strong>End Time:</strong> {test_results.get('end_time', 'N/A')}</p>
                <p><strong>Duration:</strong> {test_results.get('duration', 0):.2f}s</p>
                <p><strong>Pass Rate:</strong> {pass_rate:.1f}%</p>
            </div>
            
            <div class="metrics">
                <div class="metric">
                    <div class="metric-value">{total}</div>
                    <div class="metric-label">Total</div>
                </div>
                <div class="metric">
                    <div class="metric-value" style="color: #28a745;">{passed}</div>
                    <div class="metric-label">Passed</div>
                </div>
                <div class="metric">
                    <div class="metric-value" style="color: #dc3545;">{failed}</div>
                    <div class="metric-label">Failed</div>
                </div>
                <div class="metric">
                    <div class="metric-value" style="color: #ffc107;">{test_results.get('skipped', 0)}</div>
                    <div class="metric-label">Skipped</div>
                </div>
            </div>
            
            <div class="scenarios">
                <h2>Scenario Results</h2>
        """
        
        # Add scenario details
        for scenario in test_results.get('scenarios', []):
            status_class = scenario['status']
            body += f"""
                <div class="scenario {status_class}">
                    <strong>{scenario['name']}</strong> - {scenario['status'].upper()}
                    <br>
                    <small>Feature: {scenario.get('feature', 'N/A')} | Duration: {scenario.get('duration', 0):.2f}s</small>
            """
            
            if scenario.get('test_case_id'):
                body += f"<br><small>Test Case: {scenario['test_case_id']}</small>"
            
            if scenario['status'] == 'failed' and scenario.get('error'):
                body += f"<br><small style='color: #dc3545;'>Error: {scenario['error']}</small>"
            
            body += "</div>"
        
        body += f"""
            </div>
            
            <div class="footer">
                <p>This is an automated email from the Test Automation Framework.</p>
                <p>Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
        </body>
        </html>
        """
        
        return self.send_email(subject, body, html=True)