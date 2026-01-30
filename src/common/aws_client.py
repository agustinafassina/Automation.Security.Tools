"""
AWS client utilities for consistent boto3 client creation.
"""

import boto3
from typing import Optional
import logging

logger = logging.getLogger(__name__)


def get_ec2_client(region_name: Optional[str] = None):
    """
    Create and return an EC2 client.
    
    Args:
        region_name: AWS region name. If None, uses default region.
        
    Returns:
        boto3 EC2 client
    """
    try:
        return boto3.client('ec2', region_name=region_name)
    except Exception as e:
        logger.error(f"Error creating EC2 client for region {region_name}: {e}")
        raise


def get_iam_client(region_name: Optional[str] = None):
    """
    Create and return an IAM client.
    
    Args:
        region_name: AWS region name (IAM is global, but kept for consistency).
        
    Returns:
        boto3 IAM client
    """
    try:
        return boto3.client('iam', region_name=region_name)
    except Exception as e:
        logger.error(f"Error creating IAM client: {e}")
        raise


def get_route53_client(region_name: str = 'us-east-1'):
    """
    Create and return a Route53 client.
    
    Args:
        region_name: AWS region name (default: us-east-1).
        
    Returns:
        boto3 Route53 client
    """
    try:
        return boto3.client('route53', region_name=region_name)
    except Exception as e:
        logger.error(f"Error creating Route53 client: {e}")
        raise

