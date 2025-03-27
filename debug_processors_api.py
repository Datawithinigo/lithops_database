#!/usr/bin/env python3
"""
Debug Processors API Endpoint for GreenComputingLithops

This script specifically tests the processors API endpoint for the GreenComputingLithops project
with detailed debugging information.

Usage:
    python debug_processors_api.py [base_url]

Arguments:
    base_url: The base URL of the API (default: https://www.greencomputinglithops.es)

Example:
    python debug_processors_api.py
    python debug_processors_api.py https://greencomputinglithops.vercel.app
"""

import sys
import json
import requests
from urllib.parse import urljoin

def debug_request(url, headers=None):
    """Make a request with detailed debugging information."""
    print(f"\n=== Testing URL: {url} ===")
    
    try:
        # Make the request with verbose output
        print("Sending request...")
        response = requests.get(url, headers=headers, timeout=10)
        
        # Print response details
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {json.dumps(dict(response.headers), indent=2)}")
        
        # Try to parse as JSON
        try:
            data = response.json()
            print(f"Response Body (JSON): {json.dumps(data, indent=2)}")
            return data
        except json.JSONDecodeError:
            # If not JSON, print as text
            print(f"Response Body (text): {response.text[:500]}...")
            if len(response.text) > 500:
                print("(response truncated)")
            return response.text
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

def test_variations(base_url):
    """Test various variations of the processors endpoint."""
    endpoints = [
        "/api/processors",
        "/api/processors/",
        "/api/processors/index",
        "/api/processors/index/",
        "/api/processors/index/index",
        "/api/processors/index/index.js",
        "/api/processors?limit=10",
        "/api/processors/index?limit=10",
        "/api/processors/index/index?limit=10"
    ]
    
    results = {}
    for endpoint in endpoints:
        url = urljoin(base_url, endpoint)
        print(f"\n\n{'='*50}")
        print(f"Testing endpoint: {endpoint}")
        print(f"{'='*50}")
        
        # Test with different headers
        headers_variations = [
            None,  # No special headers
            {"Accept": "application/json"},
            {"Content-Type": "application/json"}
        ]
        
        for headers in headers_variations:
            header_desc = "default headers" if headers is None else f"headers: {headers}"
            print(f"\n--- With {header_desc} ---")
            result = debug_request(url, headers)
            results[f"{endpoint} ({header_desc})"] = "Success" if result is not None else "Failed"
    
    # Summary
    print("\n\n" + "="*50)
    print("SUMMARY OF RESULTS")
    print("="*50)
    for endpoint, result in results.items():
        print(f"{endpoint}: {result}")

def main():
    # Get base URL from command line argument or use default
    base_url = sys.argv[1] if len(sys.argv) > 1 else "https://www.greencomputinglithops.es"
    
    print(f"Debugging processors API endpoint at {base_url}")
    test_variations(base_url)
    
    print("\nDebugging complete!")

if __name__ == "__main__":
    main()
