#!/usr/bin/env python3
"""
Database Initialization Script for Simple CRM
This script creates all database tables and populates sample data.
"""

import os
import sys
import json
from datetime import datetime

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db, User, Contact, Account, Opportunity, Lead, CustomObject, CustomRecord
from werkzeug.security import generate_password_hash

def init_database():
    """Initialize the database with tables and sample data."""
    print("🗄️  Initializing Simple CRM Database...")
    
    with app.app_context():
        # Drop all tables if they exist (for clean start)
        print("🧹 Dropping existing tables...")
        db.drop_all()
        
        # Create all tables
        print("🏗️  Creating database tables...")
        db.create_all()
        
        # Create admin user
        print("👤 Creating admin user...")
        admin = User(
            username='admin',
            email='admin@crm.com',
            password_hash=generate_password_hash('admin123'),
            role='admin'
        )
        db.session.add(admin)
        db.session.commit()
        
        # Add sample data
        print("📊 Adding sample data...")
        
        # Sample Contacts
        contacts = [
            Contact(first_name='John', last_name='Doe', email='john.doe@example.com', 
                   phone='+1-555-0101', company='TechCorp', title='CEO'),
            Contact(first_name='Jane', last_name='Smith', email='jane.smith@example.com', 
                   phone='+1-555-0102', company='InnovateInc', title='CTO'),
            Contact(first_name='Mike', last_name='Johnson', email='mike.johnson@example.com', 
                   phone='+1-555-0103', company='GlobalTech', title='VP Sales'),
            Contact(first_name='Sarah', last_name='Williams', email='sarah.williams@example.com', 
                   phone='+1-555-0104', company='StartupXYZ', title='Marketing Director'),
            Contact(first_name='David', last_name='Brown', email='david.brown@example.com', 
                   phone='+1-555-0105', company='EnterpriseCo', title='Product Manager')
        ]
        db.session.add_all(contacts)
        db.session.commit()
        print(f"✅ Added {len(contacts)} sample contacts")
        
        # Sample Accounts
        accounts = [
            Account(name='TechCorp', industry='Technology', website='https://techcorp.com', 
                   phone='+1-555-0201', annual_revenue=5000000, employees=150),
            Account(name='InnovateInc', industry='Technology', website='https://innovateinc.com', 
                   phone='+1-555-0202', annual_revenue=2500000, employees=75),
            Account(name='GlobalTech', industry='Technology', website='https://globaltech.com', 
                   phone='+1-555-0203', annual_revenue=10000000, employees=300),
            Account(name='StartupXYZ', industry='Technology', website='https://startupxyz.com', 
                   phone='+1-555-0204', annual_revenue=500000, employees=25),
            Account(name='EnterpriseCo', industry='Manufacturing', website='https://enterpriseco.com', 
                   phone='+1-555-0205', annual_revenue=20000000, employees=500)
        ]
        db.session.add_all(accounts)
        db.session.commit()
        print(f"✅ Added {len(accounts)} sample accounts")
        
        # Sample Opportunities
        opportunities = [
            Opportunity(name='Enterprise Software License', account_id=1, contact_id=1, 
                       amount=50000, stage='Proposal', probability=75, 
                       description='Multi-year software license for enterprise deployment'),
            Opportunity(name='Cloud Migration Project', account_id=2, contact_id=2, 
                       amount=150000, stage='Negotiation', probability=60, 
                       description='Complete cloud infrastructure migration'),
            Opportunity(name='Custom Development', account_id=3, contact_id=3, 
                       amount=75000, stage='Qualification', probability=40, 
                       description='Custom software development for sales automation'),
            Opportunity(name='Consulting Services', account_id=4, contact_id=4, 
                       amount=25000, stage='Prospecting', probability=20, 
                       description='Technical consulting and implementation services'),
            Opportunity(name='System Integration', account_id=5, contact_id=5, 
                       amount=100000, stage='Closed Won', probability=100, 
                       description='Integration of existing systems with new platform')
        ]
        db.session.add_all(opportunities)
        db.session.commit()
        print(f"✅ Added {len(opportunities)} sample opportunities")
        
        # Sample Leads
        leads = [
            Lead(first_name='Alex', last_name='Thompson', email='alex.thompson@newcompany.com', 
                 phone='+1-555-0301', company='NewCompany', status='New', source='Website'),
            Lead(first_name='Lisa', last_name='Garcia', email='lisa.garcia@startup.com', 
                 phone='+1-555-0302', company='Startup', status='Contacted', source='Referral'),
            Lead(first_name='Tom', last_name='Wilson', email='tom.wilson@enterprise.com', 
                 phone='+1-555-0303', company='Enterprise', status='Qualified', source='Social Media'),
            Lead(first_name='Emma', last_name='Davis', email='emma.davis@tech.com', 
                 phone='+1-555-0304', company='TechCompany', status='Unqualified', source='Cold Call'),
            Lead(first_name='Chris', last_name='Miller', email='chris.miller@corp.com', 
                 phone='+1-555-0305', company='CorpInc', status='Converted', source='Email Campaign')
        ]
        db.session.add_all(leads)
        db.session.commit()
        print(f"✅ Added {len(leads)} sample leads")
        
        # Sample Custom Object
        custom_object = CustomObject(
            name='Product',
            label='Product',
            description='Product catalog for tracking inventory and sales',
            fields=json.dumps([
                {'name': 'name', 'type': 'text', 'label': 'Product Name'},
                {'name': 'sku', 'type': 'text', 'label': 'SKU'},
                {'name': 'price', 'type': 'number', 'label': 'Price'},
                {'name': 'category', 'type': 'text', 'label': 'Category'},
                {'name': 'description', 'type': 'textarea', 'label': 'Description'}
            ])
        )
        db.session.add(custom_object)
        db.session.commit()
        print("✅ Created sample custom object (Product)")
        
        # Sample Custom Records
        custom_records = [
            CustomRecord(
                object_id=custom_object.id,
                data=json.dumps({
                    'name': 'Premium Software License',
                    'sku': 'PSL-001',
                    'price': '999.99',
                    'category': 'Software',
                    'description': 'Annual premium software license with full support'
                })
            ),
            CustomRecord(
                object_id=custom_object.id,
                data=json.dumps({
                    'name': 'Cloud Storage Package',
                    'sku': 'CSP-002',
                    'price': '299.99',
                    'category': 'Cloud Services',
                    'description': '1TB cloud storage with backup and sync'
                })
            ),
            CustomRecord(
                object_id=custom_object.id,
                data=json.dumps({
                    'name': 'Consulting Hours',
                    'sku': 'CH-003',
                    'price': '150.00',
                    'category': 'Services',
                    'description': 'Professional consulting services per hour'
                })
            )
        ]
        db.session.add_all(custom_records)
        db.session.commit()
        print(f"✅ Added {len(custom_records)} sample custom records")
        
        print("\n🎉 Database initialization completed successfully!")
        print("📊 Sample data includes:")
        print(f"   • {len(contacts)} contacts")
        print(f"   • {len(accounts)} accounts") 
        print(f"   • {len(opportunities)} opportunities")
        print(f"   • {len(leads)} leads")
        print(f"   • 1 custom object with {len(custom_records)} records")
        print("\n👤 Login credentials:")
        print("   Username: admin")
        print("   Password: admin123")
        print("\n🚀 You can now run the application with: python app.py")

if __name__ == '__main__':
    try:
        init_database()
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        sys.exit(1) 