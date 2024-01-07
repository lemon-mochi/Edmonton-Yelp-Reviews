In order for the python program to run properly, the user must create a login that uses SQL Server Authentication. This can be done by right-clicking Security/Logins and creating a new login. Then the user should go to Security in Server Properties to allow SQL Server Authentication. The server must be restarted for this to take effect.

When bulk inserting, the location after 'FROM' should be changed to wherever the files are actually stored. 

To run the program, pymssql and prettyTable were installed. Both can be installed using pip3 commands in the linux terminal.

How to interact with the program:
The program runs through the termianl/shell only. It does not use any GUIs.
The program first asks the user for a username. If the username is not in the user_yelp table, the user will not gain access to the rest of the features.
The username must be an exact match with no leading or trailing spaces. The username is also case-sensetive.
After loggin in, the program asks for an input. The choices are 0, 1, 2, 3, or exit. If anything else is entered, nothing will happen.
Choosing 0 calls the search_bus() function which searches the business table.
choosing 1 calls the search_user() function which searches the user_yelp table.
2 is used to make friends. The program asks for the friend's ID. This only works if the friend's ID is valid, not the same as the user's ID, and is not already a friend.
3 is used to review a business. The program asks for the business ID and the number of stars. If the entered ID or # of stars are not valid, no review is made.
A randomly generated string of length 22 that is not already in the review table is used as the primary key of the new review.
Typing exit when the program asks for a choice will end the program.
