import tkinter as tk
from tkinter import ttk
import sqlite3
import re
from datetime import datetime
import random
from tkinter.messagebox import showinfo

class ATMApp():
    def __init__(self, root, db_name):
        self.root = root
        self.root.title("Kenneth's ATM")
        self.root.geometry("600x500")
        self.root.configure(bg="blanchedalmond")
        self.root.resizable(width=False, height=False)

        self.db_name = db_name
        self.conn = None
        self.cursor = None

        self.frame = tk.Frame(self.root, width=600, height=90, bg="firebrick")
        self.frame.pack(fill=tk.X)
        self.frame_lbl = tk.Label(self.frame, text="DELA ROSA EXCHEQUER", font=("Times new roman", 20, "bold"), bg="firebrick", fg="GOLD")
        self.frame_lbl.pack(pady=20)

        self.logindesign()
        #self.atmdesign()
        self.connect_sql()
        self.create_table()
    
    def connect_sql(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
      
    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS accountsdata (
                               Username TEXT, 
                               Password TEXT,
                               Balance INTEGER,
                               Valid_Account TEXT,
                               date DATE,
                               Account_ID INTEGER)''')  
        self.conn.commit()  
    
    def generate_password(self):
        pattern = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!@£$%^&*()0123456789"
        self.generated_password = ""

        for x in range(8):
          self.generated_password += random.choice(pattern)
        self.generated_lbl.config(text=self.generated_password)    

    def login_button(self):
        username = self.login_entry.get()
        password = self.password_entry.get()
        self.cursor.execute("SELECT 1 FROM accountsdata WHERE Username = ? AND Password = ?", (username, password))
        account_exists = self.cursor.fetchone()

        if account_exists:
            print("Login Succesful.")
            self.loginENT = self.login_entry.get()
            for widget in self.root.winfo_children():
                 if widget != self.frame:
                     widget.destroy()
            self.atmdesign()
            return
        else:
            print("Account not found.")
            
    def create_button(self):
        now = datetime.now()
        self.username = self.createusn_entry.get()
        pass0 = str(self.createpass_entry.get())
        self.password = str(self.confirmpass_entry.get())
        valid_account = self.numberORemail_entry.get()
        formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
        self.balance = 0

        usn_pattern = r"^[A-Za-z0-9_]+$"
        password_pattern = r"^[A-Za-z0-9*_$£@!.:;]+$"
        valid_account_pattern = r"^[A-Za-z0-9._]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

        valid_usn = re.match(usn_pattern, self.username)
        valid_password = re.match(password_pattern, self.password)
        valid_account2 = re.match(valid_account_pattern, valid_account)

        pattern = "1234567890"
        self.generated_id = ""

        for x in range(9):
            self.generated_id += random.choice(pattern)
        new_id = self.generated_id

        if valid_usn and len(self.username) >= 8:
            self.validation_usn.config(text="*", fg="Green")
            print("Next")
        elif valid_usn and len(self.username) <= 8: 
            self.validation_usn.config(text="Atleast 8 Characters", fg="red")
            print("must contain atleast 6 characters.")
        else:
            self.validation_usn.config(text="Invalid", fg="red")
            print("Invalid Username.")

       #PASSWORDS
        if self.password == valid_password:
            self.validation_pass.config(text="Invalid", fg="red")
            print("Invalid Password.")
        elif self.password == "":
            self.validation_pass.config(text="Invalid", fg="red")
            print("Invalid Password.")
        else:
            self.validation_pass.config(text="*", fg="Green")
            print("Next.")
      #CONFIRM PASSWORD
        if pass0 != self.password:
            self.validation_confirmP.config(text="Not match.", fg="red")
            print("Not match.")
        elif self.password == "":
            self.validation_confirmP.config(text="Invalid", fg="red")
            print("Invalid.")
        elif pass0 == self.password:
            self.validation_confirmP.config(text="*", fg="Green")
            print("Next")
            
        if valid_account2:
           self.validate_validacc.config(text="*", fg="Green")
           print("Account Created.")
        else:
           self.validate_validacc.config(text="Invalid", fg="red")
           print("Invalid Email/Number.")
        
        self.cursor.execute("SELECT 1 FROM accountsdata WHERE Username = ? AND Password = ?", (self.username, self.password))
        account_exists = self.cursor.fetchone()

        if account_exists:
            print("Account already exists.")
        elif valid_usn and valid_account2:
            self.cursor.execute("INSERT INTO accountsdata (Username, Password, Balance, Valid_Account, date, Account_ID) VALUES (?, ?, ?, ?, ?, ?)",
                                (self.username, self.password, self.balance, valid_account, formatted_date, new_id))
            self.conn.commit()
            print("Account Created.")
            for widget in self.root.winfo_children():
                if widget != self.frame:
                    widget.destroy()
            self.logindesign()
            return
        else:
            print("Try again.")
            return

    def logindesign(self):
        # LOGIN (LABEL AND ENTRY)
        self.login_lbl = tk.Label(self.root, text="Username", font=("Courier New", 18, "bold"), bg="blanchedalmond", fg="maroon")
        self.login_lbl.place(x=40, y=155)
        self.login_entry = tk.Entry(self.root, width=26, font=("Courier New", 17))
        self.login_entry.place(x=40, y=185)

        # PASSWORD (LABEL AND ENTRY)
        self.password_lbl = tk.Label(self.root, text="Password", font=("Courier New", 18, "bold"), bg="blanchedalmond", fg="maroon")
        self.password_lbl.place(x=40, y=225)
        self.password_entry = tk.Entry(self.root, width=26, font=("Courier New", 17), show="*")
        self.password_entry.place(x=40, y=255)

        # BUTTONS
        self.login_btn = tk.Button(self.root, text="Login", font=("Courier New", 18), width=8, command=self.login_button)
        self.login_btn.place(x=40, y=300)
        self.signup_button = tk.Button(self.root, text="Sign Up", font=("Courier New", 18), width=10, command=self.signupdesign)
        self.signup_button.place(x=191, y=300)

    def signupdesign(self):
        # BREAK WIDGETS
        for widget in self.root.winfo_children():
            if widget != self.frame:
                widget.destroy()

        # USERNAME (LABEL AND ENTRY)
        self.createusn_lbl = tk.Label(self.root, text="Create Username", font=("Courier New", 18, "bold"), bg="blanchedalmond", fg="maroon")
        self.createusn_lbl.place(x=15, y=90)
        self.createusn_entry = tk.Entry(self.root, width=26, font=("Courier New", 17))
        self.createusn_entry.place(x=15, y=120)

        # PASSWORD (LABEL AND ENTRY)
        self.createpass_lbl = tk.Label(self.root, text="Create Password", font=("Courier New", 18, "bold"), bg="blanchedalmond", fg="maroon")
        self.createpass_lbl.place(x=15, y=160)
        self.createpass_entry = tk.Entry(self.root, width=26, font=("Courier New", 17))
        self.createpass_entry.place(x=15, y=190)

        # GENERATED AND CREATE PASSWORD (BUTTON AND LABEL)
        self.createpass_btn = tk.Button(self.root, text="Generate", font=("Courier New", 18), width=7, command=self.generate_password)
        self.createpass_btn.place(x=15, y=230)
        self.generated_lbl = tk.Label(self.root, text="", font=("Courier New", 18, "bold"), bg="blanchedalmond", fg="maroon")
        self.generated_lbl.place(x=140, y=233)

        # CONFIRM PASS (LABEL AND ENTRY)
        self.confirmpass_lbl = tk.Label(self.root, text="Confirm Password", font=("Courier New", 18, "bold"), bg="blanchedalmond", fg="maroon")
        self.confirmpass_lbl.place(x=15, y=270)
        self.confirmpass_entry = tk.Entry(self.root, width=26, font=("Courier New", 17))
        self.confirmpass_entry.place(x=15, y=300)

        # NUMBER OR EMAIL (LABEL AND ENTRY)
        self.numberORemail_lbl = tk.Label(self.root, text="Enter Email/Number", font=("Courier New", 18, "bold"), bg="blanchedalmond", fg="maroon")
        self.numberORemail_lbl.place(x=15, y=340)
        self.numberORemail_entry = tk.Entry(self.root, width=26, font=("Courier New", 17))
        self.numberORemail_entry.place(x=15, y=370)

        # CREATE ACCOUNT BUTTON
        self.createacc_btn = tk.Button(self.root, text="Create", font=("Courier New", 18), width=10, command=self.create_button)
        self.createacc_btn.place(x=15, y=410)

        # VALID/INVALID MESSAGE
        self.validation_usn = tk.Label(self.root, text="", font=("Courier New", 18, "bold"), bg="blanchedalmond", fg="maroon")
        self.validation_usn.place(x=320, y=123)
        self.validation_pass = tk.Label(self.root, text="", font=("Courier New", 18, "bold"), bg="blanchedalmond", fg="maroon")
        self.validation_pass.place(x=320, y=193)
        self.validation_confirmP = tk.Label(self.root, text="", font=("Courier New", 18, "bold"), bg="blanchedalmond", fg="maroon")
        self.validation_confirmP.place(x=320, y=303)
        self.validate_validacc = tk.Label(self.root, text="", font=("Courier New", 18, "bold"), bg="blanchedalmond", fg="maroon")
        self.validate_validacc.place(x=320,y=373)
      
    def atmdesign(self):
      #ATM WELCOME LABEL
        self.ATM_lbl = tk.Label(self.root, text="Welcome to DRE ATM Service", font=("Courier New", 18, "bold"), bg="blanchedalmond", fg="maroon")
        self.ATM_lbl.pack()

      #WITHDRAW BUTTON
        self.withdraw_button = tk.Button(self.root, text="Withdraw", command=self.interact)
        self.withdraw_button.pack()

      #DEPOSIT BUTTON
        self.deposit_button = tk.Button(self.root, text="Deposit", command=self.interact)
        self.deposit_button.pack()

      #CHECK BALANCE BUTTON
        self.checkbalance_button = tk.Button(self.root, text="Check Balance", command=self.interact)
        self.checkbalance_button.pack()
      
      #PROFILE BUTTON
        self.profile_button = tk.Button(self.root, text="Profile")
        self.profile_button.pack()
    
    def select_number(self, number):
        self.selected_number += number
        print("Selected Number:", self.selected_number)
        self.textbox.delete("1.0", tk.END)
        self.textbox.insert(tk.END, self.selected_number)

    def checkbalance(self):
        username = self.loginENT
        self.cursor.execute('SELECT Balance FROM accountsdata WHERE Username = ?', (username,))
        check_balance = self.cursor.fetchone()
        print(f"Your Current Balance: {check_balance[0]}")
    
    def deposit(self):
        entered_amount = float(self.textbox.get("1.0", tk.END).strip())
        username = self.loginENT
        self.cursor.execute('SELECT Balance FROM accountsdata WHERE Username = ?', (username,))
        current_balance = self.cursor.fetchone()
        entered_amount += current_balance[0]
        self.cursor.execute('UPDATE accountsdata SET Balance = Balance + ? WHERE Username = ?', (entered_amount, username))
        self.conn.commit()
        print(f"Deposited: {entered_amount:.2f}")

    

    def interact(self):
      #BREAK WIDGETS
        for widget in self.root.winfo_children():
            if widget != self.frame:
                widget.destroy(),

      #KEYPAD AND TEXTBOX
        self.textBOX = tk.Text(self.root, height=10, width=34)
        self.textBOX.place(x=176, y=90)
        self.textbox = tk.Text(self.root, height=1, width=18, font=("Courier New", 20))
        self.textbox.place(x=178, y=240)
        self.textbox.insert(tk.END, "Enter Amount.")
        
        self.keypad_frame = ttk.Frame(self.root)
        self.keypad_frame.place(x=183, y=280)

        self.selected_number = ""

        numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '*', '.']

        for i, number in enumerate(numbers):
            row = i // 3
            column = i % 3
            ttk.Button(self.keypad_frame, text=number, command=lambda d=number: self.select_number(d), width=3).grid(row=row, column=column, padx=5, pady=10)

        self.checkbalance_button = tk.Button(self.root, text="Check Balance", command=self.checkbalance)
        self.checkbalance_button.pack()
        
        self.deposit_button = tk.Button(self.root, text="Deposit", command=self.deposit)
        self.deposit_button.pack()
      
 
if __name__ == "__main__":
    root = tk.Tk()
    app = ATMApp(root, 'accountsdata.db')
    root.mainloop()
