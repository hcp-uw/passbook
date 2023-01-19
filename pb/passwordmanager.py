import random
import string

passwordDict = {}

#create random password for user or user can create own password
def createPassword():
    websiteName = input("What is the name of the website you would like to make this password for? ").lower()

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
        siteLink = input("Please paste link to the login page: ")
        accountInfo = {websiteName : ["Username: " + userName, "Password: " + userPass, "Login page: " + siteLink]}
        passwordDict.update(accountInfo)
        print("Password successfully added!")
        print()

#look up the password to a website entered by the user  
def passLookup():
    websiteName = input("Please enter the name of the website you would like to look up: ").lower()

    if websiteName in passwordDict:
        print(passwordDict[websiteName])
    else:
        print("Website not found!")
    
    print()

#print all passwords
def printPassList():
    for key, value in passwordDict.items():
        print(key, value)
        print()

def changePassword():
    websiteName = input("What is the name of the website you would like to change the password to? ").lower()
    newPass = input("Enter the new password: ")

    passwordDict[websiteName][1] = "Password: " + newPass
    print()

# main 
print("Welcome to your password manager!")
masterPassword = input("Please input your master password: ")

while masterPassword != "masterpassword":
    masterPassword = input("The password you entered is incorrect, please try again: ")

print()
print("You are in!")
print()

userCommand = ""
while userCommand != "5":
    print("What would you like to do?")
    print("1. Create new password")
    print("2. Look up a password")
    print("3. Print password list")
    print("4. Change an existing password")
    print("5. Quit")
    print()
    userCommand = input("Please select an action using its corresponding number: ")
    print()
    if userCommand == "1":
        createPassword()
    elif userCommand == "2":
        passLookup()
    elif userCommand == "3":
        printPassList()
    elif userCommand == "4":
        changePassword()