#!/usr/bin/env python3
"""
Test script for Simple CRM
This script tests the basic functionality of the CRM application.
"""

import os
import sys
import json

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test if all required modules can be imported."""
    print("🧪 Testing imports...")
    
    try:
        from app import app, db, User, Contact, Account, Opportunity, Lead, CustomObject, CustomRecord
        from app import from_json, safe_json_load
        print("✅ All imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_json_filters():
    """Test the custom JSON filters."""
    print("🧪 Testing JSON filters...")
    
    try:
        from app import from_json, safe_json_load
        
        # Test from_json filter
        test_data = '{"name": "test", "value": 123}'
        result = from_json(test_data)
        assert result == {"name": "test", "value": 123}
        
        # Test safe_json_load
        result = safe_json_load(test_data)
        assert result == {"name": "test", "value": 123}
        
        # Test with None
        result = from_json(None)
        assert result == []
        
        result = safe_json_load(None)
        assert result == {}
        
        print("✅ JSON filters working correctly")
        return True
    except Exception as e:
        print(f"❌ JSON filter test failed: {e}")
        return False

def test_database_connection():
    """Test database connection and table creation."""
    print("🧪 Testing database connection...")
    
    try:
        from app import app, db
        
        with app.app_context():
            # Test if we can create tables
            db.create_all()
            print("✅ Database tables created successfully")
            
            # Test if we can query
            from app import User
            user_count = User.query.count()
            print(f"✅ Database query successful (users: {user_count})")
            
        return True
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

def test_templates():
    """Test if templates can be rendered."""
    print("🧪 Testing template rendering...")
    
    try:
        from app import app
        
        with app.app_context():
            # Test basic template rendering
            from flask import render_template_string
            
            # Test with our custom filter
            template = "{{ '{\"test\": \"value\"}' | from_json | tojson }}"
            result = render_template_string(template)
            print("✅ Template rendering with custom filter successful")
            
        return True
    except Exception as e:
        print(f"❌ Template test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 Starting Simple CRM Tests...")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_json_filters,
        test_database_connection,
        test_templates
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The CRM system is ready to use.")
        print("\n🚀 To start the application:")
        print("   python app.py")
        print("\n📱 Access at: http://localhost:5000")
        print("👤 Login: admin / admin123")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return 1
    
    return 0

if __name__ == '__main__':
    exit(main()) 