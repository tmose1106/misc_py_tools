import os

user = os.geteuid()

print(user)
if user != 0:
    print("You must be root user!")
else:
    print("Hello root user! How are you?")
