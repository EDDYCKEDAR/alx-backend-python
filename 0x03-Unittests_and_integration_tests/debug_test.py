#!/usr/bin/env python3
"""Debug script to identify test issues."""

import sys
import traceback

def test_imports():
    """Test all imports individually."""
    try:
        print("Testing imports...")
        
        print("1. Importing unittest...")
        import unittest
        print("   ✓ unittest imported successfully")
        
        print("2. Importing unittest.mock...")
        from unittest.mock import patch, Mock, PropertyMock
        print("   ✓ unittest.mock imported successfully")
        
        print("3. Importing parameterized...")
        from parameterized import parameterized, parameterized_class
        print("   ✓ parameterized imported successfully")
        
        print("4. Importing fixtures...")
        from fixtures import TEST_PAYLOAD
        print("   ✓ fixtures imported successfully")
        print(f"   TEST_PAYLOAD type: {type(TEST_PAYLOAD)}")
        print(f"   TEST_PAYLOAD length: {len(TEST_PAYLOAD)}")
        
        print("5. Importing client...")
        from client import GithubOrgClient
        print("   ✓ client imported successfully")
        print(f"   GithubOrgClient: {GithubOrgClient}")
        
        # Test instantiation
        print("6. Testing GithubOrgClient instantiation...")
        client = GithubOrgClient("google")
        print(f"   ✓ Client created: {client}")
        
        return True
        
    except Exception as e:
        print(f"   ✗ Import failed: {e}")
        print(f"   Error type: {type(e)}")
        traceback.print_exc()
        return False

def test_simple_method():
    """Test a simple method call."""
    try:
        print("\nTesting simple method call...")
        from client import GithubOrgClient
        
        client = GithubOrgClient("google")
        
        # Test static method
        result = client.has_license(
            {"license": {"key": "mit"}}, 
            "mit"
        )
        print(f"   ✓ has_license result: {result}")
        return True
        
    except Exception as e:
        print(f"   ✗ Method test failed: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=== DEBUG TEST ===")
    
    imports_ok = test_imports()
    if imports_ok:
        method_ok = test_simple_method()
        if method_ok:
            print("\n✓ All basic tests passed!")
        else:
            print("\n✗ Method test failed")
            sys.exit(1)
    else:
        print("\n✗ Import test failed")
        sys.exit(1)
