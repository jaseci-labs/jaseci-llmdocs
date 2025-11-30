#!/usr/bin/env python3
"""Test script for variant endpoints"""
import requests
import json

API_BASE = 'http://localhost:5050/api'

def test_get_variants():
    print("Testing GET /api/variants...")
    response = requests.get(f"{API_BASE}/variants")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_create_variant():
    print("Testing POST /api/variants...")
    data = {
        'variant_name': 'test-variant',
        'url': 'https://example.com/test.md',
        'version': 'v1.0.0',
        'description': 'Test variant for testing'
    }
    response = requests.post(f"{API_BASE}/variants", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_delete_variant():
    print("Testing DELETE /api/variants/test-variant...")
    response = requests.delete(f"{API_BASE}/variants/test-variant")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

if __name__ == '__main__':
    print("Make sure the API server is running on port 5050\n")

    try:
        test_get_variants()
        test_create_variant()
        test_get_variants()
        test_delete_variant()
        test_get_variants()
        print("All tests completed!")
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to API server. Make sure it's running on port 5050")
    except Exception as e:
        print(f"Error: {e}")
