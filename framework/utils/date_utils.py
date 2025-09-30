"""Date utility functions for test automation."""

from datetime import datetime, timedelta, date
from typing import Optional, Union
import arrow
from dateutil import parser
from dateutil.relativedelta import relativedelta


class DateUtils:
    """Comprehensive date utility functions."""
    
    @staticmethod
    def get_current_date(format_string: Optional[str] = None) -> Union[datetime, str]:
        """
        Get current date/time.
        
        Args:
            format_string: Optional format string (e.g., '%Y-%m-%d')
            
        Returns:
            Current datetime or formatted string
        """
        now = datetime.now()
        if format_string:
            return now.strftime(format_string)
        return now
    
    @staticmethod
    def get_past_date(
        days: int = 0,
        weeks: int = 0,
        months: int = 0,
        years: int = 0,
        from_date: Optional[datetime] = None,
        format_string: Optional[str] = None
    ) -> Union[datetime, str]:
        """
        Get past date from current date or specified date.
        
        Args:
            days: Number of days to subtract
            weeks: Number of weeks to subtract
            months: Number of months to subtract
            years: Number of years to subtract
            from_date: Starting date (default: current date)
            format_string: Optional format string
            
        Returns:
            Past datetime or formatted string
        """
        base_date = from_date or datetime.now()
        
        # Calculate past date
        past_date = base_date - timedelta(days=days, weeks=weeks)
        
        if months or years:
            past_date = past_date - relativedelta(months=months, years=years)
        
        if format_string:
            return past_date.strftime(format_string)
        return past_date
    
    @staticmethod
    def get_future_date(
        days: int = 0,
        weeks: int = 0,
        months: int = 0,
        years: int = 0,
        from_date: Optional[datetime] = None,
        format_string: Optional[str] = None
    ) -> Union[datetime, str]:
        """
        Get future date from current date or specified date.
        
        Args:
            days: Number of days to add
            weeks: Number of weeks to add
            months: Number of months to add
            years: Number of years to add
            from_date: Starting date (default: current date)
            format_string: Optional format string
            
        Returns:
            Future datetime or formatted string
        """
        base_date = from_date or datetime.now()
        
        # Calculate future date
        future_date = base_date + timedelta(days=days, weeks=weeks)
        
        if months or years:
            future_date = future_date + relativedelta(months=months, years=years)
        
        if format_string:
            return future_date.strftime(format_string)
        return future_date
    
    @staticmethod
    def compare_dates(
        date1: Union[datetime, str],
        date2: Union[datetime, str],
        date_format: Optional[str] = None
    ) -> int:
        """
        Compare two dates.
        
        Args:
            date1: First date
            date2: Second date
            date_format: Format string if dates are strings
            
        Returns:
            -1 if date1 < date2, 0 if equal, 1 if date1 > date2
        """
        # Convert strings to datetime
        if isinstance(date1, str):
            date1 = DateUtils.parse_date(date1, date_format)
        if isinstance(date2, str):
            date2 = DateUtils.parse_date(date2, date_format)
        
        if date1 < date2:
            return -1
        elif date1 > date2:
            return 1
        return 0
    
    @staticmethod
    def is_date_greater(
        date1: Union[datetime, str],
        date2: Union[datetime, str],
        date_format: Optional[str] = None
    ) -> bool:
        """
        Check if date1 is greater than date2.
        
        Args:
            date1: First date
            date2: Second date
            date_format: Format string if dates are strings
            
        Returns:
            True if date1 > date2
        """
        return DateUtils.compare_dates(date1, date2, date_format) > 0
    
    @staticmethod
    def is_date_less(
        date1: Union[datetime, str],
        date2: Union[datetime, str],
        date_format: Optional[str] = None
    ) -> bool:
        """
        Check if date1 is less than date2.
        
        Args:
            date1: First date
            date2: Second date
            date_format: Format string if dates are strings
            
        Returns:
            True if date1 < date2
        """
        return DateUtils.compare_dates(date1, date2, date_format) < 0
    
    @staticmethod
    def is_date_equal(
        date1: Union[datetime, str],
        date2: Union[datetime, str],
        date_format: Optional[str] = None
    ) -> bool:
        """
        Check if dates are equal.
        
        Args:
            date1: First date
            date2: Second date
            date_format: Format string if dates are strings
            
        Returns:
            True if dates are equal
        """
        return DateUtils.compare_dates(date1, date2, date_format) == 0
    
    @staticmethod
    def get_date_difference(
        date1: Union[datetime, str],
        date2: Union[datetime, str],
        unit: str = 'days',
        date_format: Optional[str] = None
    ) -> int:
        """
        Get difference between two dates.
        
        Args:
            date1: First date
            date2: Second date
            unit: Unit of measurement ('days', 'weeks', 'months', 'years', 'hours', 'minutes')
            date_format: Format string if dates are strings
            
        Returns:
            Difference in specified unit
        """
        # Convert strings to datetime
        if isinstance(date1, str):
            date1 = DateUtils.parse_date(date1, date_format)
        if isinstance(date2, str):
            date2 = DateUtils.parse_date(date2, date_format)
        
        delta = abs(date1 - date2)
        
        if unit == 'days':
            return delta.days
        elif unit == 'weeks':
            return delta.days // 7
        elif unit == 'months':
            return delta.days // 30  # Approximate
        elif unit == 'years':
            return delta.days // 365  # Approximate
        elif unit == 'hours':
            return int(delta.total_seconds() // 3600)
        elif unit == 'minutes':
            return int(delta.total_seconds() // 60)
        elif unit == 'seconds':
            return int(delta.total_seconds())
        else:
            raise ValueError(f"Invalid unit: {unit}")
    
    @staticmethod
    def format_date(
        date_obj: Union[datetime, str],
        output_format: str,
        input_format: Optional[str] = None
    ) -> str:
        """
        Format date to specified format.
        
        Args:
            date_obj: Date to format
            output_format: Desired output format
            input_format: Input format if date_obj is string
            
        Returns:
            Formatted date string
        """
        if isinstance(date_obj, str):
            date_obj = DateUtils.parse_date(date_obj, input_format)
        
        return date_obj.strftime(output_format)
    
    @staticmethod
    def parse_date(
        date_string: str,
        date_format: Optional[str] = None
    ) -> datetime:
        """
        Parse date string to datetime object.
        
        Args:
            date_string: Date string to parse
            date_format: Expected format (uses fuzzy parsing if not provided)
            
        Returns:
            Datetime object
        """
        if date_format:
            return datetime.strptime(date_string, date_format)
        else:
            # Use dateutil parser for flexible parsing
            return parser.parse(date_string)
    
    @staticmethod
    def get_day_of_week(
        date_obj: Union[datetime, str],
        date_format: Optional[str] = None
    ) -> str:
        """
        Get day of week for a date.
        
        Args:
            date_obj: Date to check
            date_format: Format string if date_obj is string
            
        Returns:
            Day of week (e.g., 'Monday')
        """
        if isinstance(date_obj, str):
            date_obj = DateUtils.parse_date(date_obj, date_format)
        
        return date_obj.strftime('%A')
    
    @staticmethod
    def is_weekend(
        date_obj: Union[datetime, str],
        date_format: Optional[str] = None
    ) -> bool:
        """
        Check if date is a weekend.
        
        Args:
            date_obj: Date to check
            date_format: Format string if date_obj is string
            
        Returns:
            True if Saturday or Sunday
        """
        if isinstance(date_obj, str):
            date_obj = DateUtils.parse_date(date_obj, date_format)
        
        return date_obj.weekday() in (5, 6)
    
    @staticmethod
    def is_business_day(
        date_obj: Union[datetime, str],
        date_format: Optional[str] = None
    ) -> bool:
        """
        Check if date is a business day (Monday-Friday).
        
        Args:
            date_obj: Date to check
            date_format: Format string if date_obj is string
            
        Returns:
            True if weekday
        """
        return not DateUtils.is_weekend(date_obj, date_format)
    
    @staticmethod
    def get_next_business_day(
        from_date: Optional[datetime] = None,
        format_string: Optional[str] = None
    ) -> Union[datetime, str]:
        """
        Get next business day.
        
        Args:
            from_date: Starting date (default: current date)
            format_string: Optional format string
            
        Returns:
            Next business day datetime or formatted string
        """
        base_date = from_date or datetime.now()
        next_day = base_date + timedelta(days=1)
        
        while not DateUtils.is_business_day(next_day):
            next_day += timedelta(days=1)
        
        if format_string:
            return next_day.strftime(format_string)
        return next_day
    
    @staticmethod
    def get_start_of_month(
        date_obj: Optional[datetime] = None,
        format_string: Optional[str] = None
    ) -> Union[datetime, str]:
        """
        Get start of month for given date.
        
        Args:
            date_obj: Date (default: current date)
            format_string: Optional format string
            
        Returns:
            Start of month datetime or formatted string
        """
        base_date = date_obj or datetime.now()
        start = base_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        if format_string:
            return start.strftime(format_string)
        return start
    
    @staticmethod
    def get_end_of_month(
        date_obj: Optional[datetime] = None,
        format_string: Optional[str] = None
    ) -> Union[datetime, str]:
        """
        Get end of month for given date.
        
        Args:
            date_obj: Date (default: current date)
            format_string: Optional format string
            
        Returns:
            End of month datetime or formatted string
        """
        base_date = date_obj or datetime.now()
        next_month = base_date.replace(day=28) + timedelta(days=4)
        end = next_month - timedelta(days=next_month.day)
        end = end.replace(hour=23, minute=59, second=59, microsecond=999999)
        
        if format_string:
            return end.strftime(format_string)
        return end
    
    @staticmethod
    def get_timestamp(
        date_obj: Optional[datetime] = None,
        milliseconds: bool = False
    ) -> int:
        """
        Get Unix timestamp.
        
        Args:
            date_obj: Date (default: current date)
            milliseconds: Return milliseconds instead of seconds
            
        Returns:
            Unix timestamp
        """
        base_date = date_obj or datetime.now()
        timestamp = int(base_date.timestamp())
        
        if milliseconds:
            timestamp *= 1000
        
        return timestamp
    
    @staticmethod
    def from_timestamp(
        timestamp: int,
        milliseconds: bool = False,
        format_string: Optional[str] = None
    ) -> Union[datetime, str]:
        """
        Convert Unix timestamp to datetime.
        
        Args:
            timestamp: Unix timestamp
            milliseconds: Whether timestamp is in milliseconds
            format_string: Optional format string
            
        Returns:
            Datetime or formatted string
        """
        if milliseconds:
            timestamp = timestamp / 1000
        
        date_obj = datetime.fromtimestamp(timestamp)
        
        if format_string:
            return date_obj.strftime(format_string)
        return date_obj
    
    @staticmethod
    def humanize_date(date_obj: Union[datetime, str]) -> str:
        """
        Convert date to human-readable format (e.g., '2 days ago').
        
        Args:
            date_obj: Date to humanize
            
        Returns:
            Humanized date string
        """
        if isinstance(date_obj, str):
            date_obj = DateUtils.parse_date(date_obj)
        
        return arrow.get(date_obj).humanize()