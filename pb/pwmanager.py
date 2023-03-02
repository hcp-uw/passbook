from dbtest import *

openMasterPass()

userName = input("Please input your username: ")
masterPassword = input("Please input your master password: ").encode('utf8')

opendb(userName, masterPassword)

userCommand = ""
while userCommand != "6":
    print("What would you like to do?")
    print("1. Create new password")
    print("2. Look up a password")
    print("3. Print password list")
    print("4. Change an existing password")
    print("5. Clear all passwords")
    print("6. Quit")
    print()
    userCommand = input("Please select an action using its corresponding number: ")
    print()
    if userCommand == "1":
        addPassword()
    elif userCommand == "2":
        passwordLookup()
    elif userCommand == "3":
        showPasswords()
    elif userCommand == "4":
        changePassword()
    elif userCommand == "5":
        clearPasswords()