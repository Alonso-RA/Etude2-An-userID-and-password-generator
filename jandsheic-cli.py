import os
import sys
import csv
import shutil
import secrets
import random
import string
from datetime import datetime

# The file path where the file will be created
desktop = os.path.join(os.path.expanduser("~"), "Desktop")

# This will clear the screen  when transitioning between functions
def clear():
    os.system("cls" if os.name == "nt" else "clear")

# This controls the positioning of the menu and options in screen
def centered(prompt, offset=0):
    width = shutil.get_terminal_size().columns
    pad = max((width - len(prompt)) // 2 + offset, 0)
    return " " * pad + prompt

# This is what "hears" what keys has been pressed...
def get_key():
    if os.name == 'nt':
        import msvcrt
        return msvcrt.getch().decode('utf-8', 'ignore')
    import tty, termios
    old = termios.tcgetattr(sys.stdin)
    tty.setraw(sys.stdin)
    key = sys.stdin.read(1)
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old)
    return key

#...this interprets what the above function received.
def input_esc(prompt):
    sys.stdout.write(centered(prompt))
    sys.stdout.flush()
    text = []
    while True:
        ch = get_key()
        if ch == '\x1b':
            print()
            return None
        if ch in ('\r', '\n'):
            print()
            return ''.join(text)
        if ch in ('\x08', '\x7f'):
            if text:
                text.pop()
                sys.stdout.write('\b \b')
                sys.stdout.flush()
            continue
        if ch in ('\xe0', '\x00'):
            get_key()
            continue
        text.append(ch)
        sys.stdout.write(ch)
        sys.stdout.flush()

# If there is none, this is what names the file and saves it using the path described above.
# the file name will be the combination of the wave number, month an day, i.e. batch010924.csv.

def batch_filepath():
    now = datetime.now()
    for n in range(1, 100):
        name = "batch{:02d}{:02d}{:02d}.csv".format(n, now.month, now.day)
        path = os.path.join(desktop, name)
        if not os.path.exists(path):
            return path
    return os.path.join(desktop, "batch99{:02d}{:02d}.csv".format(now.month, now.day))

# In case there is already a file, this one created the consecutive number batch010924.csv, batch020924.csv  etc.
def current_batch_filepath():
    now = datetime.now()
    existing = []
    for n in range(1, 100):
        name = "batch{:02d}{:02d}{:02d}.csv".format(n, now.month, now.day)
        path = os.path.join(desktop, name)
        if os.path.exists(path):
            existing.append(path)
    if existing:
        return existing[-1]
    return batch_filepath()

# This is what hears and awaits for the user to press F5 to create and save the file.
def wait_save():
    while True:
        save = get_key()
        if save == '\x1b':
            return False
        if save in ('\xe0', '\x00'):
            if get_key() == '?':
                return True

#A User ID for a learning center? Perhaps a EmployeeID? Here is where that is generated.
#In this example, the formula is explained in the "code" section
def generate_code():

    name = input_esc(centered("Type the first name:  ", offset=(-94)))
    if name is None:
        return None
    last_name = input_esc(centered("Type the last name:   ", offset=(-94)))
    if last_name is None:
        return None
    #The formula goes like this: The first 2 letters of the first name and  2 from the last name, the number
    #of the month and 3 random numbers, so John Rambo would have the JoRa09412 ID.
    code = (
            name[:2].lower()
            + last_name[:2].lower()
            + str(datetime.now().month).zfill(2)
            + str(random.randint(0, 999))
    )
    return name, last_name, code


#This is what generates the password. For this project, it's set to 6.
def generate_password(length=6):
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(chars) for _ in range(length))

# This is the admin screen. You can enter blocks of new people. The user will type  the name
# and last name, which are fundamental  for the code generation.
def admin_mode():
      clear()
      while True:
        print("")
        print("")
        print(centered("Press Esc to return to the main menu at any time. Once finished, press F5 to save this info in a.csv file.",  offset=(3)))
        print("")
        print("")
        n_str = input_esc(centered("Enter no. of new members:  ", offset=(-95)))
        print ("")
        if n_str is None:
            print(centered("Cancelled."))
            return []
        try:
            n = int(n_str)
        except ValueError:
            print(centered("Enter a valid number."))
            continue
        d = []
        for _ in range(n):
            result = generate_code()
            if result is None:
                print(centered("Cancelled."))
                return d
            name, last_name, code = result
            password = generate_password()
            d.append([name, last_name, code, password])
        for member in d:
            print("")
            print(centered(", ".join(member), offset=(5)))
            print("")

        if wait_save():
            path = batch_filepath()
            with open(path, "a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["first name", "last name", "user id", "password"])
                writer.writerows(d)
            print(centered("Saved to " + path))
        return d

# This is the single user or public terminal. This will  generate only one code per user.
# It will create the file of the day if not created
def terminal_mode():
    clear()
    print ("")
    print("")
    print(centered("Type your first and last name to get a user ID and a Password."))
    print("")
    print("")
    while True:
        result = generate_code()
        if result is None:
            print("")
            print(centered("Terminal mode closed."))
            print("")
            return
        name, last_name,  code = result
        password = generate_password()
        path = current_batch_filepath()
        new_file = not os.path.exists(path) or os.path.getsize(path) == 0
        with open(path, "a", newline="") as file:
            writer = csv.writer(file)
            if new_file:
                writer.writerow(["first name", "last name", "user id", "password"])
                writer.writerow([name, last_name, code, password])
        print("")
        print(centered(f"Hi, {name}, your UId is {code} and the pass is: {password}", offset=(2)))
        print("")

# This what controls the logic top to bottom
def main():
    is_running = True
    while is_running:
        clear()
        print("")
        print("")
        print("")
        print("")
        print(centered("Jandsheic"))
        print("")
        print(centered("Press the number to access the desired mode or press ESC to exit", offset=1))
        print("")
        print("")
        print(centered("1- Admin mode", offset=-1))
        print(centered("2- Terminal mode"))
        print(centered("3- Exit", offset=-4))
        choice = get_key()
        #the menu mechanism
        if choice == '1':
            admin_mode()
        elif choice == '2':
            terminal_mode()
        elif choice == '3' or choice == '\x1b':
            is_running = False
        else:
            print(centered("Get serious!"))

# The Kickstart
if __name__ == '__main__':
    main()

#Thank you for reading!