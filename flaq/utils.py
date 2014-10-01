from flaq import bcrypt

def verify_password(password_hash, password):
    """
    Verify the password hash with the password
    """
    return bcrypt.check_password_hash(password_hash, password)

def make_password_hash(password):
    """
    Create a password hash
    """
    return bcrypt.generate_password_hash(password)