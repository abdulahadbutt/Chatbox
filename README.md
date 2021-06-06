# How to run
1. open a command prompt
2. write "python server.py" and hit enter
3. open two other command prompts
4. write "python client.py" and hit enter in both of them
5. client will ask for username and password (look at usernames.csv for a list of acceptable combinations)
6. Once verified, set one client to wait by entering the '!wait' command
7. In the other client, hit R to show the list of active users
8. Select the waiting user by entering his username
9. Wait to be connected
10. Send messages one at a time
11. Enter '-1' to disconnect

# Information about the files
- client.py is the client file
- server.py is the server file
- usernames.csv contains all the usernames and passwords
- connected_users.txt is a .txt file used to contain pickle dumps of lists (More info in code)

