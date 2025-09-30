"""System resource monitoring and logging."""

import psutil
import platform
import threading
import time
import logging
from datetime import datetime
from typing import Dict, Optional


class SystemMonitor:
    """Monitor and log system resources."""
    
    def __init__(self, config_manager=None):
        """
        Initialize system monitor.
        
        Args:
            config_manager: Configuration manager instance
        """
        self.config_manager = config_manager
        self.logger = logging.getLogger('AutomationFramework.SystemMonitor')
        self.monitoring = False
        self.monitor_thread = None
        
        # Get configuration
        if config_manager:
            self.enabled = config_manager.get('system_monitoring', 'enabled', True)
            self.log_interval = config_manager.get('system_monitoring', 'log_interval_seconds', 60)
            self.capture_cpu = config_manager.get('system_monitoring', 'capture_cpu', True)
            self.capture_memory = config_manager.get('system_monitoring', 'capture_memory', True)
            self.capture_disk = config_manager.get('system_monitoring', 'capture_disk', True)
            self.capture_network = config_manager.get('system_monitoring', 'capture_network', True)
        else:
            self.enabled = True
            self.log_interval = 60
            self.capture_cpu = True
            self.capture_memory = True
            self.capture_disk = True
            self.capture_network = True
    
    def get_system_info(self) -> Dict:
        """
        Get system information.
        
        Returns:
            Dictionary with system information
        """
        info = {
            'platform': platform.system(),
            'platform_release': platform.release(),
            'platform_version': platform.version(),
            'architecture': platform.machine(),
            'processor': platform.processor(),
            'python_version': platform.python_version(),
            'hostname': platform.node(),
        }
        
        # CPU information
        info['cpu_count_logical'] = psutil.cpu_count(logical=True)
        info['cpu_count_physical'] = psutil.cpu_count(logical=False)
        
        # Memory information
        memory = psutil.virtual_memory()
        info['total_memory_gb'] = round(memory.total / (1024**3), 2)
        
        # Disk information
        disk = psutil.disk_usage('/')
        info['total_disk_gb'] = round(disk.total / (1024**3), 2)
        
        return info
    
    def log_system_info(self) -> None:
        """Log system information."""
        info = self.get_system_info()
        
        self.logger.info("=" * 80)
        self.logger.info("SYSTEM INFORMATION")
        self.logger.info("=" * 80)
        self.logger.info(f"Platform: {info['platform']} {info['platform_release']}")
        self.logger.info(f"Architecture: {info['architecture']}")
        self.logger.info(f"Processor: {info['processor']}")
        self.logger.info(f"Python Version: {info['python_version']}")
        self.logger.info(f"Hostname: {info['hostname']}")
        self.logger.info(f"CPU Cores: {info['cpu_count_physical']} physical, {info['cpu_count_logical']} logical")
        self.logger.info(f"Total Memory: {info['total_memory_gb']} GB")
        self.logger.info(f"Total Disk: {info['total_disk_gb']} GB")
        self.logger.info("=" * 80)
    
    def get_current_metrics(self) -> Dict:
        """
        Get current system metrics.
        
        Returns:
            Dictionary with current metrics
        """
        metrics = {
            'timestamp': datetime.now().isoformat()
        }
        
        # CPU metrics
        if self.capture_cpu:
            metrics['cpu_percent'] = psutil.cpu_percent(interval=1)
            metrics['cpu_per_core'] = psutil.cpu_percent(interval=1, percpu=True)
        
        # Memory metrics
        if self.capture_memory:
            memory = psutil.virtual_memory()
            metrics['memory_percent'] = memory.percent
            metrics['memory_used_gb'] = round(memory.used / (1024**3), 2)
            metrics['memory_available_gb'] = round(memory.available / (1024**3), 2)
        
        # Disk metrics
        if self.capture_disk:
            disk = psutil.disk_usage('/')
            metrics['disk_percent'] = disk.percent
            metrics['disk_used_gb'] = round(disk.used / (1024**3), 2)
            metrics['disk_free_gb'] = round(disk.free / (1024**3), 2)
        
        # Network metrics
        if self.capture_network:
            net = psutil.net_io_counters()
            metrics['bytes_sent_mb'] = round(net.bytes_sent / (1024**2), 2)
            metrics['bytes_recv_mb'] = round(net.bytes_recv / (1024**2), 2)
        
        return metrics
    
    def log_current_metrics(self) -> None:
        """Log current system metrics."""
        metrics = self.get_current_metrics()
        
        log_parts = [f"System Metrics - {metrics['timestamp']}"]
        
        if self.capture_cpu:
            log_parts.append(f"CPU: {metrics['cpu_percent']}%")
        
        if self.capture_memory:
            log_parts.append(
                f"Memory: {metrics['memory_percent']}% "
                f"({metrics['memory_used_gb']}GB used, {metrics['memory_available_gb']}GB available)"
            )
        
        if self.capture_disk:
            log_parts.append(
                f"Disk: {metrics['disk_percent']}% "
                f"({metrics['disk_used_gb']}GB used, {metrics['disk_free_gb']}GB free)"
            )
        
        if self.capture_network:
            log_parts.append(
                f"Network: {metrics['bytes_sent_mb']}MB sent, {metrics['bytes_recv_mb']}MB received"
            )
        
        self.logger.info(" | ".join(log_parts))
    
    def _monitor_loop(self) -> None:
        """Monitoring loop running in background thread."""
        while self.monitoring:
            try:
                self.log_current_metrics()
            except Exception as e:
                self.logger.error(f"Error logging metrics: {e}")
            
            time.sleep(self.log_interval)
    
    def start(self) -> None:
        """Start monitoring in background thread."""
        if not self.enabled:
            self.logger.info("System monitoring is disabled")
            return
        
        if self.monitoring:
            self.logger.warning("System monitoring is already running")
            return
        
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        self.logger.info(f"System monitoring started (interval: {self.log_interval}s)")
    
    def stop(self) -> None:
        """Stop monitoring."""
        if self.monitoring:
            self.monitoring = False
            if self.monitor_thread:
                self.monitor_thread.join(timeout=5)
            self.logger.info("System monitoring stopped")
    
    def get_process_info(self, pid: Optional[int] = None) -> Dict:
        """
        Get process information.
        
        Args:
            pid: Process ID (default: current process)
            
        Returns:
            Dictionary with process information
        """
        if pid is None:
            process = psutil.Process()
        else:
            process = psutil.Process(pid)
        
        with process.oneshot():
            info = {
                'pid': process.pid,
                'name': process.name(),
                'status': process.status(),
                'cpu_percent': process.cpu_percent(),
                'memory_percent': process.memory_percent(),
                'memory_mb': round(process.memory_info().rss / (1024**2), 2),
                'create_time': datetime.fromtimestamp(process.create_time()).isoformat(),
                'num_threads': process.num_threads(),
            }
        
        return info