# Mutual Lesson (08-04-21)

This repository contains all of the code I wrote for demonstrating credential bruteforcing. This code was written to solve the [Username enumeration via different responses](https://portswigger.net/web-security/authentication/password-based/lab-username-enumeration-via-different-responses) Portswigger lab.

## Files

* `passwords.txt` - Portswigger's provided [list of passwords](https://portswigger.net/web-security/authentication/auth-lab-passwords)
* `usernames.txt` - Portswigger's provided [list of usernames](https://portswigger.net/web-security/authentication/auth-lab-usernames)
* `enumerate_usernames.py` - Goes through `usernames.txt` and checks the error messages returned with each. If it receives an anomalous error message, it stops.
* `enumerate_passwords.py` - Goes through `passwords.txt` and checks to see which redirects, indicating that the password+username combination was correct.
* `crack.py` - Combines the methodologies of `enumerate_usernames.py` and `enumerate_passwords.py` and implements asynchronous calls to create a one-stop-shop brute-forcer for the lab.