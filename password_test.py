from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Test with your password
password = "Password123"
print(f"Password length: {len(password)} characters, {len(password. encode('utf-8'))} bytes")

# Try hashing
try:
    hashed = pwd_context.hash(password)
    print(f"✓ Hashing successful: {hashed[:50]}...")
except Exception as e:
    print(f"✗ Error: {e}")