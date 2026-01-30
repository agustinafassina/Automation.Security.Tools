"""
Configuration management for Security Automation Tools.
"""

import os
from typing import List
from dataclasses import dataclass


@dataclass
class Config:
    """Application configuration."""
    
    # AWS Regions
    aws_regions: List[str] = None
    
    # Port scanning
    default_timeout: float = 2.0
    max_workers: int = 100
    popular_ports: List[int] = None
    
    # Rate limiting
    requests_per_second: int = 10
    
    # Output
    output_dir: str = "./results"
    
    def __post_init__(self):
        """Initialize default values if not provided."""
        if self.aws_regions is None:
            self.aws_regions = [
                'us-east-1', 'us-east-2', 'us-west-1', 'us-west-2',
                'ap-south-1', 'ap-northeast-1', 'ap-northeast-2',
                'ap-northeast-3', 'ap-southeast-1', 'ap-southeast-2',
                'ca-central-1', 'eu-central-1', 'eu-west-1', 'eu-west-2',
                'eu-west-3', 'eu-north-1', 'sa-east-1'
            ]
        
        if self.popular_ports is None:
            self.popular_ports = [
                21, 22, 25, 53, 80, 110, 143, 443, 993, 995,
                3389, 3306, 5432, 5900, 8080, 8443
            ]
        
        # Allow override from environment variables
        self.output_dir = os.getenv('OUTPUT_DIR', self.output_dir)
        self.max_workers = int(os.getenv('MAX_WORKERS', self.max_workers))
        self.default_timeout = float(os.getenv('DEFAULT_TIMEOUT', self.default_timeout))


# Global configuration instance
config = Config()

