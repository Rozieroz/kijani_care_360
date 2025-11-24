#!/usr/bin/env python3
"""
Database migration script to add missing columns
"""
import sys
from pathlib import Path

# Add current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

def migrate_database():
    print("🔄 KijaniCare360 Database Migration")
    print("=" * 50)
    
    try:
        from app.core.config import settings
        from app.database.session import engine
        import sqlalchemy as sa
        
        print(f"📊 Connecting to database...")
        print(f"   URL: {settings.DATABASE_URL.split('@')[1] if '@' in settings.DATABASE_URL else 'localhost'}")
        
        # Connect to database
        with engine.connect() as conn:
            print("✅ Database connection successful")
            
            # Check if is_admin column exists
            print("🔍 Checking for missing columns...")
            
            try:
                result = conn.execute(sa.text("SELECT is_admin FROM users LIMIT 1"))
                print("✅ is_admin column already exists")
            except Exception:
                print("➕ Adding is_admin column to users table...")
                conn.execute(sa.text("ALTER TABLE users ADD COLUMN is_admin BOOLEAN DEFAULT FALSE"))
                conn.commit()
                print("✅ is_admin column added successfully")
            
            # Check other potential missing columns
            missing_columns = []
            
            # Check for total_points column (used in some models)
            try:
                result = conn.execute(sa.text("SELECT total_points FROM users LIMIT 1"))
            except Exception:
                missing_columns.append(("total_points", "INTEGER DEFAULT 0"))
            
            # Add missing columns
            for col_name, col_def in missing_columns:
                print(f"➕ Adding {col_name} column...")
                conn.execute(sa.text(f"ALTER TABLE users ADD COLUMN {col_name} {col_def}"))
                conn.commit()
                print(f"✅ {col_name} column added")
            
            print("\n🎯 Migration completed successfully!")
            print("💡 You can now use the authentication endpoints")
            
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        print("\n💡 Troubleshooting:")
        print("   1. Make sure PostgreSQL is running")
        print("   2. Check database connection in .env file")
        print("   3. Ensure database 'kijanicare360' exists")
        return False
    
    return True

if __name__ == "__main__":
    success = migrate_database()
    sys.exit(0 if success else 1)