from app.core.security import hash_password, verify_hash

def test_hash_password():
    password = "test_password"
    hashed_password = hash_password(password)
    assert isinstance(hashed_password, str)
    assert hashed_password != password



def test_verify_password():
    password = "test_password"
    hashed_password = hash_password(password)
    assert verify_hash(password, hashed_password)
    assert not verify_hash("testpassword2", hashed_password)