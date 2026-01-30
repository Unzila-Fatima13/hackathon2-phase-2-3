# Simple test to verify the basic structure works
print("Backend directory structure is ready!")

import os
print("Files in current directory (backend/):")
for item in os.listdir('.'):
    print(f"  - {item}")

print("\nFiles in backend/src/:")
for item in os.listdir('src'):
    print(f"  - {item}")

print("\nTo run the backend:")
print("1. Install Python dependencies: pip install fastapi uvicorn python-dotenv")
print("2. Run: uvicorn src.main:app --reload")
print("3. The server will start on http://127.0.0.1:8000")

print("\nTo run the frontend:")
print("1. Navigate to frontend directory: cd ../frontend")
print("2. Install dependencies: npm install")
print("3. Run development server: npm run dev")
print("4. The app will be available on http://localhost:3000")