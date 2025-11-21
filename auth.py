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
    hashed_password = hash_password(password)
    with open("user.txt","a") as f:
        f.write(f"{username}.{hashed_password}\n")
    print(f"User '{username}' registered.")

def user_exists(username):
    # TODO: Handle the case where the file doesn't exist yet

    # TODO: Read the file and check each line for the username

    return False
def login_user(username, password):
    with open("user.txt","r") as f:
        for line in f.readlines():
            user, hash = line.strip().split(',',1)
            if user == username:
                return verify_password(password,hash)
    return False


def validate_username(username):
    pass

def validate_password(password):
    pass

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
   """Main program loop."""
   print("\nWelcome to the Week 7 Authentication System!")

   while True:
      display_menu()
      choice = input("\nPlease select an option (1-3): ").strip()
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

        # Confirm password
         password_confirm = input("Confirm password: ").strip()
         if password != password_confirm:
            print("Error: Passwords do not match.")
            continue

        # Register the user
        register_user(username, password)

    elif choice == '2':
       # Login flow
       print("\n--- USER LOGIN ---")
       username = input("Enter your username: ").strip()
       password = input("Enter your password: ").strip()

      # Attempt login
      if login_user(username, password):
          print("\nYou are now logged in.")


       # Optional: Ask if they want to logout or exit
         input("\nPress Enter to return to main menu...")
    elif choice == '3':
     # Exit
      print("\nThank you for using the authentication system.")
      print("Exiting...")
      break

    else:
      print("\nError: Invalid option. Please select 1, 2, or 3.")
 if __name__ == "__main__":
     main()
