"""Zephyr Scale integration for test execution management."""

import requests
from typing import Dict, List, Optional
from datetime import datetime
from powerlogger import get_logger


class ZephyrIntegration:
    """Integration with Zephyr Scale for test execution tracking."""
    
    def __init__(self, config_manager):
        """
        Initialize Zephyr Scale integration.
        
        Args:
            config_manager: Configuration manager instance
        """
        self.config = config_manager
        self.logger = get_logger('ZephyrIntegration')
        
        # Get Zephyr configuration
        self.api_token = config_manager.get('zephyr', 'api_token')
        self.base_url = config_manager.get('zephyr', 'base_url', 
                                          'https://api.zephyrscale.smartbear.com/v2')
        self.test_cycle_key = config_manager.get('zephyr', 'test_cycle_key')
        
        if not self.api_token:
            raise ValueError("Zephyr API token is required")
        
        # Setup headers
        self.headers = {
            'Authorization': f'Bearer {self.api_token}',
            'Content-Type': 'application/json'
        }
        
        self.logger.info("Zephyr Scale integration initialized")
    
    def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict] = None
    ) -> Optional[Dict]:
        """
        Make HTTP request to Zephyr API.
        
        Args:
            method: HTTP method (GET, POST, PUT, etc.)
            endpoint: API endpoint
            data: Request data
            
        Returns:
            Response data or None
        """
        url = f"{self.base_url}/{endpoint}"
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=self.headers)
            elif method == 'POST':
                response = requests.post(url, headers=self.headers, json=data)
            elif method == 'PUT':
                response = requests.put(url, headers=self.headers, json=data)
            else:
                raise ValueError(f"Unsupported method: {method}")
            
            response.raise_for_status()
            return response.json() if response.text else {}
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"API request failed: {e}")
            if hasattr(e.response, 'text'):
                self.logger.error(f"Response: {e.response.text}")
            return None
    
    def get_test_case(self, test_case_key: str) -> Optional[Dict]:
        """
        Get test case details.
        
        Args:
            test_case_key: Test case key
            
        Returns:
            Test case details or None
        """
        result = self._make_request('GET', f'testcases/{test_case_key}')
        if result:
            self.logger.info(f"Retrieved test case: {test_case_key}")
        return result
    
    def get_test_cycle(self, cycle_key: Optional[str] = None) -> Optional[Dict]:
        """
        Get test cycle details.
        
        Args:
            cycle_key: Test cycle key (uses configured cycle if not provided)
            
        Returns:
            Test cycle details or None
        """
        cycle_key = cycle_key or self.test_cycle_key
        if not cycle_key:
            self.logger.error("No test cycle key provided")
            return None
        
        result = self._make_request('GET', f'testcycles/{cycle_key}')
        if result:
            self.logger.info(f"Retrieved test cycle: {cycle_key}")
        return result
    
    def create_test_execution(
        self,
        test_case_key: str,
        test_cycle_key: Optional[str] = None,
        status: str = 'Pass',
        comment: Optional[str] = None,
        environment: Optional[str] = None,
        actual_result: Optional[str] = None
    ) -> Optional[str]:
        """
        Create test execution.
        
        Args:
            test_case_key: Test case key
            test_cycle_key: Test cycle key
            status: Execution status ('Pass', 'Fail', 'Blocked', 'Not Executed')
            comment: Execution comment
            environment: Test environment
            actual_result: Actual test result
            
        Returns:
            Execution ID or None
        """
        cycle_key = test_cycle_key or self.test_cycle_key
        
        data = {
            'testCaseKey': test_case_key,
            'statusName': status,
            'testCycleKey': cycle_key,
            'executedById': 'automation',
            'executionTime': datetime.now().isoformat()
        }
        
        if comment:
            data['comment'] = comment
        
        if environment:
            data['environmentName'] = environment
        
        if actual_result:
            data['actualResult'] = actual_result
        
        result = self._make_request('POST', 'testexecutions', data)
        
        if result and 'id' in result:
            execution_id = result['id']
            self.logger.info(f"Created test execution {execution_id} for {test_case_key}")
            return execution_id
        
        return None
    
    def update_test_execution(
        self,
        test_case_key: str,
        status: str,
        comment: Optional[str] = None,
        test_cycle_key: Optional[str] = None
    ) -> bool:
        """
        Update or create test execution.
        
        Args:
            test_case_key: Test case key
            status: Execution status
            comment: Execution comment
            test_cycle_key: Test cycle key
            
        Returns:
            True if successful
        """
        execution_id = self.create_test_execution(
            test_case_key=test_case_key,
            test_cycle_key=test_cycle_key,
            status=status,
            comment=comment
        )
        
        return execution_id is not None
    
    def get_test_executions(
        self,
        test_cycle_key: Optional[str] = None,
        test_case_key: Optional[str] = None
    ) -> List[Dict]:
        """
        Get test executions.
        
        Args:
            test_cycle_key: Filter by test cycle
            test_case_key: Filter by test case
            
        Returns:
            List of test executions
        """
        params = []
        
        if test_cycle_key:
            params.append(f'testCycle={test_cycle_key}')
        elif self.test_cycle_key:
            params.append(f'testCycle={self.test_cycle_key}')
        
        if test_case_key:
            params.append(f'testCase={test_case_key}')
        
        endpoint = 'testexecutions'
        if params:
            endpoint += '?' + '&'.join(params)
        
        result = self._make_request('GET', endpoint)
        
        if result and 'values' in result:
            return result['values']
        
        return []
    
    def update_test_cycle_status(
        self,
        cycle_key: Optional[str] = None,
        status: str = 'Done'
    ) -> bool:
        """
        Update test cycle status.
        
        Args:
            cycle_key: Test cycle key
            status: Cycle status
            
        Returns:
            True if successful
        """
        cycle_key = cycle_key or self.test_cycle_key
        
        if not cycle_key:
            self.logger.error("No test cycle key provided")
            return False
        
        data = {'statusName': status}
        result = self._make_request('PUT', f'testcycles/{cycle_key}', data)
        
        if result:
            self.logger.info(f"Updated test cycle {cycle_key} status to {status}")
            return True
        
        return False
    
    def bulk_update_executions(
        self,
        executions: List[Dict[str, str]]
    ) -> bool:
        """
        Bulk update test executions.
        
        Args:
            executions: List of execution dictionaries with test_case_key and status
            
        Returns:
            True if successful
        """
        success_count = 0
        
        for execution in executions:
            test_case_key = execution.get('test_case_key')
            status = execution.get('status', 'Pass')
            comment = execution.get('comment')
            
            if test_case_key:
                if self.update_test_execution(test_case_key, status, comment):
                    success_count += 1
        
        self.logger.info(f"Updated {success_count}/{len(executions)} executions")
        return success_count == len(executions)
    
    def get_test_results_summary(
        self,
        test_cycle_key: Optional[str] = None
    ) -> Optional[Dict]:
        """
        Get summary of test results for a cycle.
        
        Args:
            test_cycle_key: Test cycle key
            
        Returns:
            Summary dictionary or None
        """
        executions = self.get_test_executions(test_cycle_key)
        
        if not executions:
            return None
        
        summary = {
            'total': len(executions),
            'passed': 0,
            'failed': 0,
            'blocked': 0,
            'not_executed': 0
        }
        
        for execution in executions:
            status = execution.get('statusName', '').lower()
            if status == 'pass':
                summary['passed'] += 1
            elif status == 'fail':
                summary['failed'] += 1
            elif status == 'blocked':
                summary['blocked'] += 1
            else:
                summary['not_executed'] += 1
        
        summary['pass_rate'] = (summary['passed'] / summary['total'] * 100) if summary['total'] > 0 else 0
        
        return summary
    
    def create_test_cycle(
        self,
        name: str,
        project_key: str,
        folder_id: Optional[str] = None,
        description: Optional[str] = None
    ) -> Optional[str]:
        """
        Create a new test cycle.
        
        Args:
            name: Cycle name
            project_key: Jira project key
            folder_id: Folder ID
            description: Cycle description
            
        Returns:
            Created cycle key or None
        """
        data = {
            'name': name,
            'projectKey': project_key
        }
        
        if folder_id:
            data['folderId'] = folder_id
        
        if description:
            data['description'] = description
        
        result = self._make_request('POST', 'testcycles', data)
        
        if result and 'key' in result:
            cycle_key = result['key']
            self.logger.info(f"Created test cycle: {cycle_key}")
            return cycle_key
        
        return None