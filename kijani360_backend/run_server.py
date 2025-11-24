#!/usr/bin/env python3
"""
KijaniCare360 Backend Server Startup Script
"""
import uvicorn
import os
import sys
from pathlib import Path
import sys   # <-- added

# Add the app directory to Python path
app_dir = Path(__file__).parent
sys.path.insert(0, str(app_dir))

def main():
    """Run the FastAPI server"""
    print("🌱 Starting KijaniCare360 Backend Server...")
    print("📍 Make sure PostgreSQL is running and database 'kijanicare360' exists")
    print("🔑 Add your GROQ_API_KEY to .env file for full AI functionality")
    print("📚 API Documentation will be available at: http://localhost:8000/docs")
    print("🌐 Frontend should connect to: http://localhost:8000/api/v1")
    print("-" * 60)
    
    # Check if .env file exists
    env_file = app_dir / ".env"
    if not env_file.exists():
        print("⚠️  Warning: .env file not found. Creating from template...")
        example_env = app_dir / ".env.example"
        if example_env.exists():
            import shutil
            shutil.copy(example_env, env_file)
            print("✅ Created .env file. Please edit it with your settings.")
        else:
            print("❌ .env.example not found. Please create .env manually.")
    
    try:
        uvicorn.run(
            "app.main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n🌳 KijaniCare360 Backend stopped gracefully.")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        print("💡 Make sure all dependencies are installed: pip install -r requirements.txt")

if __name__ == "__main__":
    main()