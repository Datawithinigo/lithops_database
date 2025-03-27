#!/usr/bin/env python3
"""
Test API Endpoints for GreenComputingLithops

This script tests various API endpoints for the GreenComputingLithops project.
It can be used to diagnose issues with the API endpoints.

Usage:
    python test_api.py [base_url]

Arguments:
    base_url: The base URL of the API (default: https://www.greencomputinglithops.es)

Example:
    python test_api.py
    python test_api.py https://greencomputinglithops.vercel.app
"""

import sys
import json
import requests
from urllib.parse import urljoin, quote

def test_endpoint(base_url, endpoint, description):
    """Test an API endpoint and print the result."""
    url = urljoin(base_url, endpoint)
    print(f"\n--- Testing {description} ---")
    print(f"URL: {url}")
    
    try:
        response = requests.get(url, timeout=10)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                if isinstance(data, list):
                    print(f"Success! Received {len(data)} items.")
                    if len(data) > 0:
                        print(f"First item: {json.dumps(data[0], indent=2)}")
                else:
                    print(f"Success! Response: {json.dumps(data, indent=2)}")
            except json.JSONDecodeError:
                print(f"Response (text): {response.text[:200]}...")
        else:
            print(f"Error: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

def test_tdp_endpoint(base_url, processor_name, endpoint_type="json"):
    """Test the TDP endpoint for a specific processor."""
    encoded_name = quote(processor_name)
    
    if endpoint_type == "json":
        endpoint = f"/api/processor/tdp/{encoded_name}"
        description = f"TDP JSON Endpoint for '{processor_name}'"
    elif endpoint_type == "plain":
        endpoint = f"/api/processor/tdp/plain/{encoded_name}"
        description = f"TDP Plain Text Endpoint for '{processor_name}'"
    elif endpoint_type == "value":
        endpoint = f"/api/processor/tdp/value/{encoded_name}"
        description = f"TDP Raw Value Endpoint for '{processor_name}'"
    
    test_endpoint(base_url, endpoint, description)

def main():
    # Get base URL from command line argument or use default
    base_url = sys.argv[1] if len(sys.argv) > 1 else "https://www.greencomputinglithops.es"
    
    # Test API endpoints
    print(f"Testing API endpoints at {base_url}")
    
    # Test processors endpoint
    test_endpoint(base_url, "/api/processors", "Processors Endpoint")
    
    # Test processors endpoint with limit
    test_endpoint(base_url, "/api/processors?limit=5", "Processors Endpoint with Limit")
    
    # Test setup-db endpoint
    test_endpoint(base_url, "/api/setup-db", "Setup DB Endpoint")
    
    # Test TDP endpoints for a sample processor
    processor_name = "Intel Xeon E5-2690"
    test_tdp_endpoint(base_url, processor_name, "json")
    test_tdp_endpoint(base_url, processor_name, "plain")
    test_tdp_endpoint(base_url, processor_name, "value")
    
    # Test index endpoint
    test_endpoint(base_url, "/api", "Index Endpoint")
    
    print("\nAPI testing complete!")

if __name__ == "__main__":
    main()
