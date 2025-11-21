import bcrypt
import os
USER_DATA_FILE = "users.txt"

def hash_password(input_password):
	#Converting the password to bytes
	password_bytes = input_password.encode("utf-8")
	#Generate a salt and hash the password
	salt = bcrypt.gensalt()
	hashed_password = bcrypt.hashpw(password_bytes, salt)
	# Decode the hash back to a string to store in a text file
	return hashed_password

def verify_password(input_password, hashed_password):
    # Encode both the plaintext password and stored hash to bytes
    password_bytes = input_password.encode("utf-8")
    hashed_password_bytes = hashed_password.encode("utf-8")
    # bcrypt.checkpw handles extracting the salt and comparing
    return bcrypt.checkpw(password_bytes, hashed_password_bytes)

def register_user(username, password):
    if os.path.exists("user.txt"):
        with open ("user.txt","r") as f:
            for line in f:
                stored_username = line.strip().split(",")[0]
                if stored_username == username:
                    print("Error: Username already registered.")
                    return False

    hashed_password = hash_password(password).decode("utf-8")
    with open("user.txt","a") as f:
        f.write(f"{username},{hashed_password}\n")
    print(f"User '{username}' registered.")
    return True

def user_exists(username):
    # Check if not exist
    if not os.path.exists("user.txt"):
        return False
    # Read file and check each line
    with open("user.txt","r") as f:
        for line in f:
            stored_username = line.strip().split(",")[0]
            if stored_username == username:
                return True
    return False
def login_user(username, password):
    # Check if file exist
    if not os.path.exists("user.txt"):
        print("Error: Username not found.")
        return False
    #Search for username in the file
    with open("user.txt","r") as f:
        for line in f:
            stored_username, stored_hash = line.strip().split(",")
            if stored_username == username:
                #Verify the password
                if verify_password(password, stored_hash.encode("utf-8")):
                    print("Login successful.")
                    return True
                else:
                    print("Incorrect password.")
                    return False
    return False
def validate_username(username):
    #Checking if username is empty
    if username == "":
        return False
        print ("Username cannot be empty.")

    if len(username)<3:
        return False
        print("Username must be at least 3 character long")

    if len(username)> 10:
        return False
        print("Username cannot be longer than 10 characters")
   #Check characters
    for char in username:
        if not char.isalnum():
            return False
        print("Username can only contain letters and numbers.")

    return True
def validate_password(password):
    if password == "":
        return False
        print("Password cannot be empty")

    if len(password) < 8:
        return False
        print("Password must be least 8 characters long")
    else:
        print("Password is invalid.")
