#!/usr/bin/env python3
"""
AgriPulse AI - Docker Health Check Script
Performs comprehensive health checks for the containerized application
"""
import sys
import os
import time
import json
from typing import Dict, Any, List

def check_streamlit_health() -> Dict[str, Any]:
    """Check if Streamlit server is responding."""
    try:
        import requests
        response = requests.get(
            'http://localhost:8501/_stcore/health',
            timeout=5
        )
        return {
            'status': 'healthy' if response.status_code == 200 else 'unhealthy',
            'status_code': response.status_code,
            'response_time_ms': response.elapsed.total_seconds() * 1000
        }
    except Exception as e:
        return {
            'status': 'unhealthy',
            'error': str(e)
        }

def check_google_api() -> Dict[str, Any]:
    """Check if Google API key is configured."""
    try:
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key or api_key.startswith('your_'):
            return {
                'status': 'unhealthy',
                'error': 'Google API key not configured'
            }
        return {
            'status': 'healthy',
            'configured': True
        }
    except Exception as e:
        return {
            'status': 'unhealthy',
            'error': str(e)
        }

def check_snowflake_config() -> Dict[str, Any]:
    """Check if Snowflake configuration is present."""
    try:
        required_vars = [
            'SNOWFLAKE_USER',
            'SNOWFLAKE_ACCOUNT',
            'SNOWFLAKE_ROLE',
            'SNOWFLAKE_WAREHOUSE',
            'SNOWFLAKE_DATABASE',
            'SNOWFLAKE_SCHEMA'
        ]
        
        missing = []
        for var in required_vars:
            value = os.getenv(var)
            if not value or value.startswith('your_'):
                missing.append(var)
        
        if missing:
            return {
                'status': 'unhealthy',
                'error': f'Missing Snowflake config: {", ".join(missing)}'
            }
        
        # Check if private key file exists
        key_file = os.getenv('SNOWFLAKE_PRIVATE_KEY_FILE', '/app/secrets/snowflake_key.pem')
        if not os.path.exists(key_file):
            return {
                'status': 'unhealthy',
                'error': f'Snowflake private key not found: {key_file}'
            }
        
        return {
            'status': 'healthy',
            'configured': True
        }
    except Exception as e:
        return {
            'status': 'unhealthy',
            'error': str(e)
        }

def check_database_connection() -> Dict[str, Any]:
    """Check if database connection is working."""
    try:
        from adk_app.core.database import get_snowflake_manager
        
        manager = get_snowflake_manager()
        if manager.test_connection():
            return {
                'status': 'healthy',
                'connected': True
            }
        else:
            return {
                'status': 'unhealthy',
                'error': 'Database connection test failed'
            }
    except Exception as e:
        return {
            'status': 'unhealthy',
            'error': str(e)
        }

def check_disk_space() -> Dict[str, Any]:
    """Check available disk space."""
    try:
        import shutil
        total, used, free = shutil.disk_usage('/')
        
        free_gb = free / (1024 ** 3)
        free_percent = (free / total) * 100
        
        if free_percent < 10:
            status = 'unhealthy'
        elif free_percent < 20:
            status = 'warning'
        else:
            status = 'healthy'
        
        return {
            'status': status,
            'free_gb': round(free_gb, 2),
            'free_percent': round(free_percent, 2)
        }
    except Exception as e:
        return {
            'status': 'unknown',
            'error': str(e)
        }

def check_memory() -> Dict[str, Any]:
    """Check memory usage."""
    try:
        import psutil
        
        memory = psutil.virtual_memory()
        memory_percent = memory.percent
        
        if memory_percent > 90:
            status = 'unhealthy'
        elif memory_percent > 80:
            status = 'warning'
        else:
            status = 'healthy'
        
        return {
            'status': status,
            'used_percent': round(memory_percent, 2),
            'available_mb': round(memory.available / (1024 ** 2), 2)
        }
    except ImportError:
        return {
            'status': 'unknown',
            'error': 'psutil not available'
        }
    except Exception as e:
        return {
            'status': 'unknown',
            'error': str(e)
        }

def run_health_checks(quick: bool = False) -> Dict[str, Any]:
    """Run all health checks."""
    checks = {
        'timestamp': time.time(),
        'checks': {}
    }
    
    # Critical checks (always run)
    checks['checks']['streamlit'] = check_streamlit_health()
    checks['checks']['google_api'] = check_google_api()
    checks['checks']['snowflake_config'] = check_snowflake_config()
    
    # Extended checks (skip in quick mode)
    if not quick:
        checks['checks']['database'] = check_database_connection()
        checks['checks']['disk_space'] = check_disk_space()
        checks['checks']['memory'] = check_memory()
    
    # Determine overall status
    statuses = [check['status'] for check in checks['checks'].values()]
    
    if 'unhealthy' in statuses:
        checks['overall_status'] = 'unhealthy'
    elif 'warning' in statuses:
        checks['overall_status'] = 'warning'
    else:
        checks['overall_status'] = 'healthy'
    
    return checks

def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='AgriPulse AI Health Check')
    parser.add_argument('--quick', action='store_true', help='Run quick checks only')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    parser.add_argument('--exit-code', action='store_true', help='Exit with code 1 if unhealthy')
    
    args = parser.parse_args()
    
    # Run health checks
    results = run_health_checks(quick=args.quick)
    
    # Output results
    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print(f"\n{'='*60}")
        print(f"AgriPulse AI Health Check")
        print(f"{'='*60}\n")
        
        print(f"Overall Status: {results['overall_status'].upper()}\n")
        
        for check_name, check_result in results['checks'].items():
            status_symbol = {
                'healthy': '✓',
                'warning': '⚠',
                'unhealthy': '✗',
                'unknown': '?'
            }.get(check_result['status'], '?')
            
            print(f"{status_symbol} {check_name.replace('_', ' ').title()}: {check_result['status']}")
            
            if 'error' in check_result:
                print(f"  Error: {check_result['error']}")
            
            # Print additional details
            for key, value in check_result.items():
                if key not in ['status', 'error']:
                    print(f"  {key}: {value}")
            print()
    
    # Exit with appropriate code
    if args.exit_code and results['overall_status'] == 'unhealthy':
        sys.exit(1)
    
    sys.exit(0)

if __name__ == '__main__':
    main()
