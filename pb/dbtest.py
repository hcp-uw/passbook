import sqlite3 
import random 
import string 
#test2
#connect to database and create a cursor which allows you to modify and get information from the database
conn = sqlite3.connect('password_manager.db')
cursor = conn.cursor()

#opendb method, takes masterpassword entered as a parameter (see pwmanager.py for funciton call)
#if masterpassword entered equals masterpassword set by user (not updated yet, masterpassword is just "masterpassword" for now)
#attempt to create a database called password with columns (website, username, and password) all of type TEXT
#if the database exists, prints "You are in!"
#conn.commit() must be called every time you make a change to a database, in this case you are making a database if it doesn't exist
def opendb(masterpassword):
    if(masterpassword == "masterpassword"):
        try:
            cursor.execute(' ' 'CREATE TABLE password (website TEXT PRIMARY KEY, username TEXT, password TEXT)' ' ')
        except:
            print("You are in!")
            print()

    conn.commit()


def addPassword():
    #prompts user for website name
    websiteName = input("What is the name of the website you would like to add a password for? ").lower() 

    #select from website column in database password where the website name is equal to that entered by the user
    #data stores all websites found in database password where the website name matches that eneterd by the user
    #fetchall() gets everything found, there is also fetchone() and fetchmany()
    cursor.execute("SELECT website FROM password WHERE website=?", (websiteName,))
    data = cursor.fetchall()

    #if website is found, print login information exists

    #else prompt user to enter their own password or have one generated for them
    #if user wants to create own password ask for password and confirm password
    #generate password using string lib containing ascii, digits, punctuation, length of password between 10 and 15

    #if user confirms password or password is generated, ask user for username
    #query variable contains command to insert user input into database
    #cursor.execture() to insert user input into the database
    #conn.commit() to confirm changes in database
    if data:
        print("Login information for website already exists!")
        print()
    else:
        userOption = input("Would you like to create your own password or have one generated for you? Please type \"create\" or \"generate\": ").lower()

        userpass = ""
        confirmPass = ""

        if userOption == "create":
            userPass = input("Please enter the password: ")
            confirmPass = input("Please retype password for confirmation: ")

            while(confirmPass != userPass):
                confirmPass = input("Password doesn't match, please try again: ")
        else:
            userPass = "".join(random.choices(string.ascii_letters + string.digits + string.punctuation, k = random.randrange(10, 15)))
    

        if userPass == confirmPass or userOption == "generate":
            userName = input("Please input username: ")
            query = "INSERT INTO password(website, username, password) VALUES (?,?,?);"
            cursor.execute(query, (websiteName, userName, userPass))
            conn.commit()
            print("Password successfully added!")
            print()


#query variable contains command to select all entries in password database where website equals user input
#when retreiving information from database "*" means select all
#if nothing is found in password database with a matching website name, print no login information
#else prompt user for a new password
#update variable contains command to update password database and set the column password to user input where website is equal to user input
#update password to new password given site name
def changePassword():
    websiteName = input("Please enter the name of the website you would like to change the password to: ").lower()
    query = "SELECT * FROM password WHERE website=?"
    cursor.execute(query, (websiteName,))
    data = cursor.fetchall()
    if not data:
        print("No login information for this website exists!")
    else:
        newPassword = input("What is the new password? ")
        update = "UPDATE password SET password=? WHERE website=?"
        cursor.execute(update, [newPassword, websiteName])
        print("Password changed successfully!")
        conn.commit()

    print()

#get all websites from database password where website name matches that entered by user
#print login information that is found, if nothing found print information doesn't exist
def passwordLookup():
    websiteName = input("Please enter the name of the website you would like to look up the password to: ").lower()
    cursor.execute("SELECT * FROM password WHERE website=?", (websiteName,))
    data = cursor.fetchall()
    if data:
        print(data)
    else:
        print("Login information for the site doesn't exist!")

    print()

#deletes all passwords from database password
#cursor.rowcount tells you how many rows in database password was deleted
def clearPasswords():
    cursor.execute("DELETE FROM password;",)
    print("You have deleted", cursor.rowcount, "records from your password database!")
    print()
    conn.commit()

#selects all rows from password database
#prints every row in password database
def showPasswords():
    cursor.execute("SELECT * FROM password")
    result = cursor.fetchall()
    for row in result:
        print(row)
        print("\n")