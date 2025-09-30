"""Jira integration for test management."""

import logging
from typing import Dict, List, Optional
from jira import JIRA


class JiraIntegration:
    """Integration with Jira for test case management."""
    
    def __init__(self, config_manager):
        """
        Initialize Jira integration.
        
        Args:
            config_manager: Configuration manager instance
        """
        self.config = config_manager
        self.logger = logging.getLogger('AutomationFramework.JiraIntegration')
        
        # Get Jira configuration
        self.server = config_manager.get('jira', 'server')
        self.email = config_manager.get('jira', 'email')
        self.api_token = config_manager.get('jira', 'api_token')
        self.project_key = config_manager.get('jira', 'project_key')
        
        if not all([self.server, self.email, self.api_token]):
            raise ValueError("Jira configuration incomplete: server, email, and api_token required")
        
        # Connect to Jira
        try:
            self.jira = JIRA(
                server=self.server,
                basic_auth=(self.email, self.api_token)
            )
            self.logger.info(f"Connected to Jira: {self.server}")
        except Exception as e:
            self.logger.error(f"Failed to connect to Jira: {e}")
            raise
    
    def get_issue(self, issue_key: str) -> Optional[Dict]:
        """
        Get Jira issue details.
        
        Args:
            issue_key: Issue key (e.g., 'PROJ-123')
            
        Returns:
            Issue details dictionary or None
        """
        try:
            issue = self.jira.issue(issue_key)
            return {
                'key': issue.key,
                'summary': issue.fields.summary,
                'description': issue.fields.description,
                'status': issue.fields.status.name,
                'priority': issue.fields.priority.name if issue.fields.priority else None,
                'assignee': issue.fields.assignee.displayName if issue.fields.assignee else None,
                'reporter': issue.fields.reporter.displayName if issue.fields.reporter else None,
                'created': str(issue.fields.created),
                'updated': str(issue.fields.updated),
            }
        except Exception as e:
            self.logger.error(f"Failed to get issue {issue_key}: {e}")
            return None
    
    def create_issue(
        self,
        summary: str,
        description: str,
        issue_type: str = 'Bug',
        priority: str = 'Medium',
        labels: Optional[List[str]] = None
    ) -> Optional[str]:
        """
        Create a new Jira issue.
        
        Args:
            summary: Issue summary
            description: Issue description
            issue_type: Issue type (Bug, Task, Story, etc.)
            priority: Priority level
            labels: List of labels
            
        Returns:
            Created issue key or None
        """
        try:
            issue_dict = {
                'project': {'key': self.project_key},
                'summary': summary,
                'description': description,
                'issuetype': {'name': issue_type},
            }
            
            if priority:
                issue_dict['priority'] = {'name': priority}
            
            if labels:
                issue_dict['labels'] = labels
            
            new_issue = self.jira.create_issue(fields=issue_dict)
            self.logger.info(f"Created issue: {new_issue.key}")
            return new_issue.key
            
        except Exception as e:
            self.logger.error(f"Failed to create issue: {e}")
            return None
    
    def create_defect(
        self,
        summary: str,
        description: str,
        test_case_key: Optional[str] = None,
        priority: str = 'High',
        screenshot_path: Optional[str] = None
    ) -> Optional[str]:
        """
        Create a defect/bug issue.
        
        Args:
            summary: Defect summary
            description: Defect description
            test_case_key: Related test case key
            priority: Priority level
            screenshot_path: Path to screenshot attachment
            
        Returns:
            Created defect key or None
        """
        labels = ['automated_test']
        if test_case_key:
            labels.append(f'test_{test_case_key}')
        
        # Add test case reference to description
        if test_case_key:
            description = f"Test Case: {test_case_key}\n\n{description}"
        
        defect_key = self.create_issue(
            summary=summary,
            description=description,
            issue_type='Bug',
            priority=priority,
            labels=labels
        )
        
        # Attach screenshot if provided
        if defect_key and screenshot_path:
            self.add_attachment(defect_key, screenshot_path)
        
        return defect_key
    
    def add_attachment(self, issue_key: str, file_path: str) -> bool:
        """
        Add attachment to Jira issue.
        
        Args:
            issue_key: Issue key
            file_path: Path to file to attach
            
        Returns:
            True if successful
        """
        try:
            with open(file_path, 'rb') as f:
                self.jira.add_attachment(issue=issue_key, attachment=f)
            self.logger.info(f"Added attachment to {issue_key}: {file_path}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to add attachment to {issue_key}: {e}")
            return False
    
    def add_comment(self, issue_key: str, comment: str) -> bool:
        """
        Add comment to Jira issue.
        
        Args:
            issue_key: Issue key
            comment: Comment text
            
        Returns:
            True if successful
        """
        try:
            self.jira.add_comment(issue_key, comment)
            self.logger.info(f"Added comment to {issue_key}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to add comment to {issue_key}: {e}")
            return False
    
    def transition_issue(self, issue_key: str, transition: str) -> bool:
        """
        Transition issue to new status.
        
        Args:
            issue_key: Issue key
            transition: Transition name or ID
            
        Returns:
            True if successful
        """
        try:
            self.jira.transition_issue(issue_key, transition)
            self.logger.info(f"Transitioned {issue_key} to {transition}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to transition {issue_key}: {e}")
            return False
    
    def get_test_cases(self, labels: Optional[List[str]] = None) -> List[Dict]:
        """
        Get test cases from Jira.
        
        Args:
            labels: Filter by labels
            
        Returns:
            List of test case dictionaries
        """
        try:
            jql = f'project = {self.project_key} AND issuetype = Test'
            
            if labels:
                label_filter = ' OR '.join([f'labels = "{label}"' for label in labels])
                jql += f' AND ({label_filter})'
            
            issues = self.jira.search_issues(jql, maxResults=1000)
            
            test_cases = []
            for issue in issues:
                test_cases.append({
                    'key': issue.key,
                    'summary': issue.fields.summary,
                    'status': issue.fields.status.name,
                    'labels': issue.fields.labels
                })
            
            return test_cases
            
        except Exception as e:
            self.logger.error(f"Failed to get test cases: {e}")
            return []
    
    def link_issues(
        self,
        inward_issue: str,
        outward_issue: str,
        link_type: str = 'Relates'
    ) -> bool:
        """
        Create link between two issues.
        
        Args:
            inward_issue: Inward issue key
            outward_issue: Outward issue key
            link_type: Link type name
            
        Returns:
            True if successful
        """
        try:
            self.jira.create_issue_link(
                type=link_type,
                inwardIssue=inward_issue,
                outwardIssue=outward_issue
            )
            self.logger.info(f"Linked {inward_issue} to {outward_issue}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to link issues: {e}")
            return False