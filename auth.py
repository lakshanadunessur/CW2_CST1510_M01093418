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
    if os.path.exists("DATA/user.txt"):
        with open ("DATA/user.txt", "r") as f:
            for line in f:
                stored_username = line.strip().split(",")[0]
                if stored_username == username:
                    print("Error: Username already registered.")
                    return False

    hashed_password = hash_password(password).decode("utf-8")
    with open("DATA/user.txt", "a") as f:
        f.write(f"{username},{hashed_password}\n")
    print(f"User '{username}' registered.")
    return True

#Function to check if user exists
def user_exists(username):
    # Check if not exist
    if not os.path.exists("DATA/user.txt"):
        return False
    # Read file and check each line
    with open("DATA/user.txt", "r") as f:
        for line in f:
            stored_username = line.strip().split(",")[0]
            if stored_username == username:
                return True
    return False
def login_user(username, password):
    # Check if file exist
    if not os.path.exists("DATA/user.txt"):
        print("Error: Username not found.")
        return False
    #Search for username in the file
    with open("DATA/user.txt", "r") as f:
        for line in f:
            stored_username, stored_hash = line.strip().split(",")
            if stored_username == username:
                #Verify the password
                if verify_password(password, stored_hash):
                    print("Login successful.")
                    return True
                else:
                    print("Incorrect password.")
                    return False

    return False
#Function to validate username
def validate_username(username):
    #Checking if username is empty
    if username == "":
        return False, "Username cannot be empty."
    if len(username) < 3:
        return False, "Username must be at least 3 characters long."
    if len(username) > 10:
        return False, "Username cannot be longer than 10 characters."
    for char in username:
        if not char.isalnum():
            return False, "Username can only contain letters and numbers."
    return True, None

   #Check if characters
    for char in username:
        if not char.isalnum():
            print("Username can only contain letters and numbers.")
            return False

    return True
#Function to validate password
def validate_password(password):
    if password == "":
        return False, "Password cannot be empty."
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    return True, None


def display_menu():
     """Displays the main menu options."""
     print("\n" + "="*50)
     print(" MULTI-DOMAIN INTELLIGENCE PLATFORM")
     print(" Secure Authentication System")
     print("="*50)
     print("\n[1] Register a new user")
     print("[2] Login")
     print("[3] Exit")
     print("-"*50)

def main():
   print("\nWelcome to the Week 7 Authentication System!")

   while True:
      display_menu()
      choice = input("\nPlease select an option (1-3): ").strip()
      #Select choices
      if choice == '1':                   #Registration flow
           print("\n--- USER REGISTRATION ---")
           username = input("Enter a username: ").strip()

      # Validate username
           is_valid, error_msg = validate_username(username)
           if not is_valid:
               print(f"Error: {error_msg}")
               continue
           password = input("Enter a password: ").strip()
           # Validate password
           is_valid, error_msg = validate_password(password)
           if not is_valid:
              print(f"Error: {error_msg}")
              continue
           password_confirm = input("Confirm password: ").strip()
           if password != password_confirm:
                  print("Error: Passwords do not match.")
                  continue
           register_user(username, password)
      elif choice == '2':
                  print("\n--- USER LOGIN ---")
                  username = input("Enter your username: ").strip()
                  password = input("Enter your password: ").strip()
                  if login_user(username, password):
                      print("\nYou are now logged in.")
                      input("\nPress Enter to return to main menu...")
      elif choice == '3':
                  print("\nThank you for using the authentication system.")
                  print("Exiting...")
                  break
      else:
                  print("\nError: Invalid option. Please select 1, 2, or 3.")
if __name__ == "__main__":
      main()