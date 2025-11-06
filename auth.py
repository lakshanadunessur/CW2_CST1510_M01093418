import bcrypt
import os
#Hashes a password using bcrypt with automatic salt generation.
#Args: In [ ]: In [ ]:
#plain_text_password (str): The plaintext password to hash
#Returns str: The hashed password as a UTF-8 string

def hash_password(plain_text_password):
	# Encode the password to bytes, required by bcrypt
 	 password_bytes = plain_text_password.encode("utf-8")
	# Generate a salt and hash the password
 	 salt = bcrypt.gensalt()
 	 hashed_password = bcrypt.hashpw(password_bytes, salt)
	# Decode the hash back to a string to store in a text file
	 return hashed_password

def verify_password(plain_text_password, hashed_password):
	# Encode both the plaintext password and stored hash to bytes
 	password_bytes = plain_text_password.encode("utf-8")
 	hashed_password_bytes = hashed_password.encode("utf-8")
	# bcrypt.checkpw handles extracting the salt and comparing
	return bcrypt.checkpw(password_bytes, hashed_password_bytes)

def register_user(username, password): 
        """Register a new user.""" 
        hashed_password = hash_password(password) 
       with open("users.txt", "a") as f: 
                f.write(f"{username},{hashed_password}\n") 
      print(f"User '{username}' registered.")
      
def login_user(username, password): 
       """Log in an existing user.""”
        with open("users.txt", "r") as f: 
                 for line in f.readlines(): 
                        user, hash = line.strip().split(',', 1) 
                         if user == username:
	return verify_password(password, hash) 
           return False
