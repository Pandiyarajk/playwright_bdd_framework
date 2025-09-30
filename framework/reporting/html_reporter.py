"""HTML report generation."""

from pathlib import Path
from typing import Dict
from datetime import datetime
import json


class HTMLReporter:
    """Generate HTML reports for test execution."""
    
    @staticmethod
    def generate_report(test_results: Dict, output_path: str = 'reports/report.html') -> str:
        """
        Generate HTML report.
        
        Args:
            test_results: Test results dictionary
            output_path: Output file path
            
        Returns:
            Path to generated report
        """
        # Calculate statistics
        total = test_results.get('total', 0)
        passed = test_results.get('passed', 0)
        failed = test_results.get('failed', 0)
        skipped = test_results.get('skipped', 0)
        pass_rate = (passed / total * 100) if total > 0 else 0
        
        # Determine overall status
        if failed > 0:
            status = 'FAILED'
            status_color = '#dc3545'
        elif passed == total:
            status = 'PASSED'
            status_color = '#28a745'
        else:
            status = 'PARTIAL'
            status_color = '#ffc107'
        
        # Generate HTML
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Test Automation Report</title>
            <style>
                * {{
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }}
                
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background-color: #f5f5f5;
                    padding: 20px;
                }}
                
                .container {{
                    max-width: 1200px;
                    margin: 0 auto;
                    background-color: white;
                    border-radius: 8px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                    overflow: hidden;
                }}
                
                .header {{
                    background: linear-gradient(135deg, {status_color} 0%, {status_color}dd 100%);
                    color: white;
                    padding: 30px;
                }}
                
                .header h1 {{
                    margin-bottom: 10px;
                }}
                
                .status-badge {{
                    display: inline-block;
                    padding: 5px 15px;
                    background-color: rgba(255,255,255,0.2);
                    border-radius: 20px;
                    font-size: 14px;
                    font-weight: bold;
                }}
                
                .metrics {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                    gap: 20px;
                    padding: 30px;
                    background-color: #f8f9fa;
                }}
                
                .metric-card {{
                    background-color: white;
                    padding: 20px;
                    border-radius: 8px;
                    text-align: center;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
                }}
                
                .metric-value {{
                    font-size: 48px;
                    font-weight: bold;
                    margin-bottom: 5px;
                }}
                
                .metric-label {{
                    color: #6c757d;
                    font-size: 14px;
                    text-transform: uppercase;
                    letter-spacing: 1px;
                }}
                
                .summary {{
                    padding: 30px;
                }}
                
                .summary-item {{
                    display: flex;
                    justify-content: space-between;
                    padding: 10px 0;
                    border-bottom: 1px solid #dee2e6;
                }}
                
                .summary-label {{
                    font-weight: 600;
                    color: #495057;
                }}
                
                .scenarios {{
                    padding: 30px;
                }}
                
                .scenario-card {{
                    border: 1px solid #dee2e6;
                    border-left: 4px solid #6c757d;
                    border-radius: 4px;
                    padding: 15px;
                    margin-bottom: 15px;
                    background-color: #f8f9fa;
                }}
                
                .scenario-card.passed {{
                    border-left-color: #28a745;
                }}
                
                .scenario-card.failed {{
                    border-left-color: #dc3545;
                }}
                
                .scenario-header {{
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin-bottom: 10px;
                }}
                
                .scenario-name {{
                    font-weight: 600;
                    font-size: 16px;
                }}
                
                .scenario-status {{
                    padding: 4px 12px;
                    border-radius: 12px;
                    font-size: 12px;
                    font-weight: bold;
                    text-transform: uppercase;
                }}
                
                .scenario-status.passed {{
                    background-color: #d4edda;
                    color: #155724;
                }}
                
                .scenario-status.failed {{
                    background-color: #f8d7da;
                    color: #721c24;
                }}
                
                .scenario-details {{
                    font-size: 14px;
                    color: #6c757d;
                }}
                
                .scenario-error {{
                    margin-top: 10px;
                    padding: 10px;
                    background-color: #fff3cd;
                    border-left: 3px solid #ffc107;
                    font-family: 'Courier New', monospace;
                    font-size: 12px;
                    color: #856404;
                }}
                
                .footer {{
                    padding: 20px 30px;
                    background-color: #f8f9fa;
                    border-top: 1px solid #dee2e6;
                    text-align: center;
                    color: #6c757d;
                    font-size: 12px;
                }}
                
                .progress-bar {{
                    width: 100%;
                    height: 8px;
                    background-color: #e9ecef;
                    border-radius: 4px;
                    overflow: hidden;
                    margin-top: 10px;
                }}
                
                .progress-bar-fill {{
                    height: 100%;
                    background-color: #28a745;
                    transition: width 0.3s ease;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Test Automation Report</h1>
                    <span class="status-badge">{status}</span>
                    <div class="progress-bar">
                        <div class="progress-bar-fill" style="width: {pass_rate}%"></div>
                    </div>
                </div>
                
                <div class="metrics">
                    <div class="metric-card">
                        <div class="metric-value">{total}</div>
                        <div class="metric-label">Total</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value" style="color: #28a745;">{passed}</div>
                        <div class="metric-label">Passed</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value" style="color: #dc3545;">{failed}</div>
                        <div class="metric-label">Failed</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value" style="color: #ffc107;">{skipped}</div>
                        <div class="metric-label">Skipped</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">{pass_rate:.1f}%</div>
                        <div class="metric-label">Pass Rate</div>
                    </div>
                </div>
                
                <div class="summary">
                    <h2>Execution Summary</h2>
                    <div class="summary-item">
                        <span class="summary-label">Start Time:</span>
                        <span>{test_results.get('start_time', 'N/A')}</span>
                    </div>
                    <div class="summary-item">
                        <span class="summary-label">End Time:</span>
                        <span>{test_results.get('end_time', 'N/A')}</span>
                    </div>
                    <div class="summary-item">
                        <span class="summary-label">Duration:</span>
                        <span>{test_results.get('duration', 0):.2f}s</span>
                    </div>
                </div>
                
                <div class="scenarios">
                    <h2>Scenario Results</h2>
        """
        
        # Add scenario cards
        for scenario in test_results.get('scenarios', []):
            status_class = scenario['status']
            html_content += f"""
                    <div class="scenario-card {status_class}">
                        <div class="scenario-header">
                            <span class="scenario-name">{scenario['name']}</span>
                            <span class="scenario-status {status_class}">{scenario['status']}</span>
                        </div>
                        <div class="scenario-details">
                            Feature: {scenario.get('feature', 'N/A')} | 
                            Duration: {scenario.get('duration', 0):.2f}s
            """
            
            if scenario.get('test_case_id'):
                html_content += f" | Test Case: {scenario['test_case_id']}"
            
            if scenario.get('tags'):
                html_content += f" | Tags: {', '.join(scenario['tags'])}"
            
            html_content += "</div>"
            
            if scenario['status'] == 'failed' and scenario.get('error'):
                html_content += f"""
                        <div class="scenario-error">
                            {scenario['error']}
                        </div>
                """
            
            html_content += "</div>"
        
        html_content += f"""
                </div>
                
                <div class="footer">
                    <p>Generated by Playwright Python BDD Framework</p>
                    <p>Report generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Write to file
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text(html_content, encoding='utf-8')
        
        return str(output_file)