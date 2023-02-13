import sqlite3 
import random 
import string 
import bcrypt
from cryptography.fernet import Fernet
import pbkdf2
import bcrypt
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
from cryptography.hazmat.backends import default_backend
import pprint

#connect to database and create a cursor which allows you to modify and get information from the database
conn = sqlite3.connect('password_manager.db')
cursor = conn.cursor()

passwordTableName = ''

def openMasterPass():
    try:    
        cursor.execute(' ' 'CREATE TABLE masterpassword (username TEXT PRIMARY KEY, masterpw TEXT, dbname TEXT)' ' ')
        print("Welcome to your password manager. Please create an account!")
        addMasterPass()
    except:
        print("Welcome back to your password manager!")
        createNew = input("Would you like to sign up or sign in? ")
        if createNew == "sign up":
            addMasterPass()
        


def addMasterPass():
    global passwordTableName
    userName = input("Enter a username: ")
    masterPass = input("Enter your master password: ")
        
    hashedPass = bcrypt.hashpw(masterPass.encode('utf8'), bcrypt.gensalt())

    randomName = ''.join(random.choices(string.ascii_lowercase, k=5))

    query = "INSERT INTO masterpassword(username, masterpw, dbname) VALUES (?,?,?);"
    cursor.execute(query, (userName, hashedPass, randomName))
    conn.commit()

    # this is keyDerivation, didn't want to make it a nested method bc parameters
    # generate another salt
    salt = os.urandom(16)
    # generate derivation function
    kdf = PBKDF2HMAC (
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100,
        backend=default_backend()
    )

    # pull hashed mp from db
    cursor.execute("SELECT masterpw FROM masterpassword WHERE username=?", (userName,))
    storedMPass = bytes(cursor.fetchone()[0])
    key = base64.urlsafe_b64encode(kdf.derive(storedMPass))

    # store as another tuple in db? globalize?
    # this is not working vvvvv
    cursor.execute("INSERT INTO masterpassword (username, masterpw, dbname) VALUES (?,?,?)", ("keyDerivation", key, randomName))
    # query = "INSERT INTO " + passwordTableName + " (website, username, password) VALUES (?,?,?);"
    # cursor.execute(query, ("keyDerivation", "username", key))
    conn.commit()
                   
#opendb method, takes masterpassword entered as a parameter (see pwmanager.py for funciton call)
#if masterpassword entered equals masterpassword set by user (not updated yet, masterpassword is just "masterpassword" for now)
#attempt to create a database called password with columns (website, username, and password) all of type TEXT
#if the database exists, prints "You are in!"
#conn.commit() must be called every time you make a change to a database, in this case you are making a database if it doesn't exist
def opendb(userName, masterPassword):
    global passwordTableName 
    cursor.execute("SELECT masterpw FROM masterpassword WHERE username=?", (userName,))
    data = cursor.fetchone()

    if(bcrypt.checkpw(masterPassword, bytes(data[0]))):
        try:
            cursor.execute("SELECT dbname FROM masterpassword WHERE username=?", (userName,))
            name = cursor.fetchone()
            passwordTableName = name[0]
            command = ' ' 'CREATE TABLE ' + passwordTableName + ' (website TEXT PRIMARY KEY, username TEXT, password TEXT)' ' '
            cursor.execute(command)
            conn.commit()
        except:
            print("You are in!")
            print()


def addPassword():
    global passwordTableName
    #prompts user for website name
    websiteName = input("What is the name of the website you would like to add a password for? ").lower() 

    #select from website column in database password where the website name is equal to that entered by the user
    #data stores all websites found in database password where the website name matches that eneterd by the user
    #fetchall() gets everything found, there is also fetchone() and fetchmany()
    command = "SELECT website FROM " + passwordTableName + " WHERE website=?"
    cursor.execute(command, (websiteName,))
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
            userPass = encryptPW(userPass)
            query = "INSERT INTO " + passwordTableName + " (website, username, password) VALUES (?,?,?);"
            cursor.execute(query, (websiteName, userName, userPass))
            conn.commit()
            print("Password successfully added!")
            print()

# encrypts pw
def encryptPW(inputPW):
    cursor.execute('SELECT masterpw FROM masterpassword WHERE username="keyDerivation"')
    keyDeriv = (cursor.fetchone()[0])
    encryptObject = Fernet(keyDeriv)
    return encryptObject.encrypt(inputPW.encode('utf-8'))

# decrypts ofc
def decryptPW(inputPW):
    inputPW = ((inputPW[0])[2])
    cursor.execute('SELECT masterpw FROM masterpassword WHERE username="keyDerivation"')
    keyDeriv = bytes(cursor.fetchone()[0])
    decryptionObject = Fernet(keyDeriv)
    return (decryptionObject.decrypt(inputPW).decode())


#query variable contains command to select all entries in password database where website equals user input
#when retreiving information from database "*" means select all
#if nothing is found in password database with a matching website name, print no login information
#else prompt user for a new password
#update variable contains command to update password database and set the column password to user input where website is equal to user input
#update password to new password given site name
def changePassword():
    global passwordTableName
    websiteName = input("Please enter the name of the website you would like to change the password to: ").lower()
    query = "SELECT * FROM " + passwordTableName + " WHERE website=?"
    cursor.execute(query, (websiteName,))
    data = cursor.fetchall()
    if not data:
        print("No login information for this website exists!")
    else:
        newPassword = input("What is the new password? ")
        update = "UPDATE " + passwordTableName + " SET password=? WHERE website=?"
        newPassword = encryptPW(newPassword)
        cursor.execute(update, [newPassword, websiteName])
        print("Password changed successfully!")
        conn.commit()

    print()

#get all websites from database password where website name matches that entered by user
#print login information that is found, if nothing found print information doesn't exist
def passwordLookup():
    global passwordTableName
    websiteName = input("Please enter the name of the website you would like to look up the password to: ").lower()
    cursor.execute("SELECT * FROM " + passwordTableName + " WHERE website=?", (websiteName,))
    data = cursor.fetchall()
    data = decryptPW(data)
    if data:
        print(data)
    else:
        print("Login information for the site doesn't exist!")

    print()

#deletes all passwords from database password
#cursor.rowcount tells you how many rows in database password was deleted
def clearPasswords():
    global passwordTableName
    cursor.execute("DELETE FROM " + passwordTableName + ";",)
    print("You have deleted", cursor.rowcount, "records from your password database!")
    print()
    conn.commit()

# this is going to have to be edited a bit because passwords are encrypted in db
#selects all rows from password database
#prints every row in password database
def showPasswords():
    global passwordTableName
    cursor.execute("SELECT * FROM " + passwordTableName)
    result = cursor.fetchall()
    for row in result:
        print(row)
        print("\n")