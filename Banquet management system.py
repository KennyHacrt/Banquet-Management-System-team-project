import mysql.connector
from mysql.connector import errorcode
from datetime import datetime
import re
import os
import sys

# Custom Exceptions for Navigation
class ExitToMainMenu(Exception):
    pass

class ExitToPreviousSection(Exception):
    pass

# Database configuration
db_config = {
    'user': 'root',         # Replace with your MySQL username
    'password': 'Jk200516!',     # Replace with your MySQL password
    'host': 'localhost',
    'database': 'bms_db',            # The database name for BMS
    'raise_on_warnings': True
}

try:
    # Connect to MySQL server
    conn = mysql.connector.connect(
        user=db_config['user'],
        password=db_config['password'],
        host=db_config['host']
    )
    cursor = conn.cursor()

    # Create the database if it doesn't exist
    cursor.execute("CREATE DATABASE IF NOT EXISTS {}".format(db_config['database']))
    conn.database = db_config['database']

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Invalid credentials. Please check your username and password.")
    else:
        print(err)
    exit(1)

def clear_terminal():
    # Clears the terminal screen
    os.system('cls' if os.name == 'nt' else 'clear')

def get_non_empty_string(prompt):
    while True:
        value = input(prompt).strip()
        if value.lower() == 'exit.m':
            raise ExitToMainMenu
        elif value.lower() == 'exit.p':
            raise ExitToPreviousSection
        if value:
            return value
        else:
            print("Input cannot be empty. Please try again or type 'exit.m'/'exit.p' to navigate.")

def get_validated_input(prompt, validation_func, error_message):
    while True:
        value = input(prompt).strip()
        if value.lower() == 'exit.m':
            raise ExitToMainMenu
        elif value.lower() == 'exit.p':
            raise ExitToPreviousSection
        if validation_func(value):
            return value
        else:
            print(error_message)

def get_choice_input(prompt, choices):
    choices_str = "/".join(choices)
    prompt = f"{prompt} ({choices_str}): "
    while True:
        value = input(prompt).strip().lower()
        if value == 'exit.m':
            raise ExitToMainMenu
        elif value == 'exit.p':
            raise ExitToPreviousSection
        if value in choices:
            return value
        else:
            print(f"Invalid choice. Please choose from {choices_str} or type 'exit.m' to return to the main menu, 'exit.p' to return to the previous menu.")

def get_integer_input(prompt, min_value=None, max_value=None):
    while True:
        value = input(prompt).strip()
        if value.lower() == 'exit.m':
            raise ExitToMainMenu
        elif value.lower() == 'exit.p':
            raise ExitToPreviousSection
        try:
            int_value = int(value)
            if (min_value is not None and int_value < min_value) or (max_value is not None and int_value > max_value):
                range_msg = f" between {min_value} and {max_value}" if min_value is not None and max_value is not None else (
                    f" >= {min_value}" if min_value is not None else f" <= {max_value}"
                )
                print(f"Please enter an integer{range_msg} or type 'exit.m'/'exit.p' to navigate.")
                continue
            return int_value
        except ValueError:
            print("Invalid input. Please enter a valid integer or type 'exit.m' to return to the main menu, 'exit.p' to return to the previous menu.")

def get_float_input(prompt, min_value=None, max_value=None):
    while True:
        value = input(prompt).strip()
        if value.lower() == 'exit.m':
            raise ExitToMainMenu
        elif value.lower() == 'exit.p':
            raise ExitToPreviousSection
        try:
            float_value = float(value)
            if (min_value is not None and float_value < min_value) or (max_value is not None and float_value > max_value):
                range_msg = f" between {min_value} and {max_value}" if min_value is not None and max_value is not None else (
                    f" >= {min_value}" if min_value is not None else f" <= {max_value}"
                )
                print(f"Please enter a number{range_msg} or type 'exit.m'/'exit.p' to navigate.")
                continue
            return float_value
        except ValueError:
            print("Invalid input. Please enter a valid number or type 'exit.m' to return to the main menu, 'exit.p' to return to the previous menu.")

def get_email_input(prompt):
    email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    prompt = prompt + " (format: xxx@xxx.xxx): "
    return get_validated_input(
        prompt,
        lambda x: re.fullmatch(email_regex, x) is not None,
        "Invalid email address. Please try again or type 'exit.m' to return to the main menu, 'exit.p' to return to the previous menu."
    )

def get_mobile_number(prompt):
    prompt = prompt + " (format: 8-digit number): "
    return get_validated_input(
        prompt,
        lambda x: re.fullmatch(r'\d{8}', x) is not None,
        "Mobile Number must be an 8-digit number. Please try again or type 'exit.m' to return to the main menu, 'exit.p' to return to the previous menu."
    )

def create_tables():
    # Dictionary of table creation statements
    TABLES = {}

    TABLES['New_banquet'] = (
        "CREATE TABLE IF NOT EXISTS New_banquet ("
        "  BIN INT AUTO_INCREMENT PRIMARY KEY,"
        "  Banquet_Name VARCHAR(255) NOT NULL,"
        "  Date DATE NOT NULL,"
        "  Time TIME NOT NULL,"
        "  Location VARCHAR(255) NOT NULL,"
        "  Available ENUM('Y','N') NOT NULL,"
        "  Quota INT NOT NULL,"
        "  Address VARCHAR(255) NOT NULL,"
        "  Contact_First_Name VARCHAR(255) NOT NULL,"
        "  Contact_Last_Name VARCHAR(255) NOT NULL"
        ") ENGINE=InnoDB"
    )

    TABLES['Meal'] = (
        "CREATE TABLE IF NOT EXISTS Meal ("
        "  Dish_Name VARCHAR(255) NOT NULL,"
        "  BIN INT NOT NULL,"
        "  Type VARCHAR(255) NOT NULL,"
        "  Special_Cuisine VARCHAR(255),"
        "  Price DECIMAL(10,2) NOT NULL,"
        "  FOREIGN KEY (BIN) REFERENCES New_banquet(BIN) ON DELETE CASCADE"
        ") ENGINE=InnoDB"
    )

    TABLES['Attendee'] = (
        "CREATE TABLE IF NOT EXISTS Attendee ("
        "  Attendee_ID INT AUTO_INCREMENT PRIMARY KEY,"
        "  First_Name VARCHAR(255) NOT NULL,"
        "  Last_Name VARCHAR(255) NOT NULL,"
        "  Address VARCHAR(255) NOT NULL,"
        "  Mobile_Number VARCHAR(8) NOT NULL,"
        "  Email_Address VARCHAR(255) NOT NULL UNIQUE,"
        "  Password VARCHAR(255) NOT NULL,"
        "  Attendee_Type ENUM('staff','student','alumni','guest') NOT NULL,"
        "  Affiliated_Organization ENUM('PolyU','SPEED','HKCC','Others') NOT NULL"
        ") ENGINE=InnoDB"
    )

    TABLES['Administrator'] = (
        "CREATE TABLE IF NOT EXISTS Administrator ("
        "  Administrator_ID INT AUTO_INCREMENT PRIMARY KEY,"
        "  First_Name VARCHAR(255) NOT NULL,"
        "  Last_Name VARCHAR(255) NOT NULL,"
        "  Address VARCHAR(255) NOT NULL,"
        "  Mobile_Number VARCHAR(8) NOT NULL,"
        "  Email_Address VARCHAR(255) NOT NULL UNIQUE,"
        "  Password VARCHAR(255) NOT NULL"
        ") ENGINE=InnoDB"
    )

    TABLES['Registration'] = (
        "CREATE TABLE IF NOT EXISTS Registration ("
        "  Registration_ID INT AUTO_INCREMENT PRIMARY KEY,"
        "  Attendee_ID INT NOT NULL,"
        "  BIN INT NOT NULL,"
        "  Seat_No INT NOT NULL,"
        "  Time DATETIME NOT NULL,"
        "  Meal_Choice VARCHAR(255) NOT NULL,"
        "  Drink_Choice ENUM('tea','coffee','lemon tea') NOT NULL,"
        "  Remarks VARCHAR(255),"
        "  FOREIGN KEY (Attendee_ID) REFERENCES Attendee(Attendee_ID) ON DELETE CASCADE,"
        "  FOREIGN KEY (BIN) REFERENCES New_banquet(BIN) ON DELETE CASCADE"
        ") ENGINE=InnoDB"
    )

    # Create tables
    for table_name in TABLES:
        table_description = TABLES[table_name]
        try:
            # print(f"Creating table {table_name}: ", end='')
            cursor.execute(table_description)
            # print("OK")
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                # print("already exists.")
                pass
            else:
                print(err.msg)

    conn.commit()

def admin_login(email, password):
    query = "SELECT * FROM Administrator WHERE Email_Address=%s AND Password=%s"
    cursor.execute(query, (email, password))
    admin = cursor.fetchone()
    if admin:
        print("Administrator logged in successfully.")
        return admin[0]  # Return Administrator_ID
    else:
        print("Invalid credentials.")
        return None

def create_banquet():
    try:
        clear_terminal()
        # Input banquet details
        print("\nCreate a New Banquet")
        print("Exit Options: Type 'exit.m' to return to the Main Menu, 'exit.p' to return to the previous menu.")
        Banquet_Name = get_non_empty_string("Banquet Name: ")

        Date_input = get_validated_input(
            "Date (YYYY-MM-DD): ",
            lambda x: re.fullmatch(r'\d{4}-\d{2}-\d{2}', x) is not None and validate_date(x),
            "Invalid date format. Please enter in YYYY-MM-DD format or type 'exit.m'/'exit.p' to navigate."
        )

        Time_input = get_validated_input(
            "Time (HH:MM:SS): ",
            lambda x: re.fullmatch(r'\d{2}:\d{2}:\d{2}', x) is not None and validate_time(x),
            "Invalid time format. Please enter in HH:MM:SS format or type 'exit.m'/'exit.p' to navigate."
        )

        Address = get_non_empty_string("Address: ")
        Location = get_non_empty_string("Location: ")

        Available = get_choice_input("Available", ['y', 'n']).upper()

        Quota = get_integer_input("Quota: ", min_value=1)

        Contact_First_Name = get_non_empty_string("Contact Staff First Name: ")
        Contact_Last_Name = get_non_empty_string("Contact Staff Last Name: ")

        # Insert into New_banquet
        insert_banquet = (
            "INSERT INTO New_banquet "
            "(Banquet_Name, Date, Time, Location, Available, Quota, Address, Contact_First_Name, Contact_Last_Name) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        )
        banquet_data = (Banquet_Name, Date_input, Time_input, Location, Available, Quota, Address, Contact_First_Name, Contact_Last_Name)
        cursor.execute(insert_banquet, banquet_data)
        conn.commit()

        # Get the BIN of the newly created banquet
        BIN = cursor.lastrowid
        print(f"Banquet created with BIN: {BIN}")

        # Input meals
        meals = []
        print("\nEnter four meals for the banquet:")
        for i in range(1, 5):
            print(f"\nMeal {i}:")
            Dish_Name = get_non_empty_string("  Dish Name: ")
            Type = get_non_empty_string("  Type (e.g., fish, chicken): ")
            # Special Cuisine is optional, allow empty
            while True:
                try:
                    Special_Cuisine = input("  Special Cuisine (optional): ").strip()
                    if Special_Cuisine.lower() == 'exit.m':
                        raise ExitToMainMenu
                    elif Special_Cuisine.lower() == 'exit.p':
                        raise ExitToPreviousSection
                    break
                except ExitToMainMenu:
                    raise
                except ExitToPreviousSection:
                    raise
            Price = get_float_input("  Price: ", min_value=0)
            meals.append((Dish_Name, BIN, Type, Special_Cuisine if Special_Cuisine else None, Price))

        # Insert meals into Meal table
        insert_meal = (
            "INSERT INTO Meal "
            "(Dish_Name, BIN, Type, Special_Cuisine, Price) "
            "VALUES (%s, %s, %s, %s, %s)"
        )
        cursor.executemany(insert_meal, meals)
        conn.commit()
        print("Meals added successfully.")
    except ExitToMainMenu:
        raise
    except ExitToPreviousSection:
        raise

def validate_date(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def validate_time(time_str):
    try:
        datetime.strptime(time_str, "%H:%M:%S")
        return True
    except ValueError:
        return False

def update_banquet():
    try:
        clear_terminal()
        print("\nUpdate Existing Banquet")
        print("Exit Options: Type 'exit.m' to return to the Main Menu, 'exit.p' to return to the previous menu.")
        BIN = get_integer_input("Enter BIN of the banquet to update: ", min_value=1)
        # Check if banquet exists
        query = "SELECT * FROM New_banquet WHERE BIN=%s"
        cursor.execute(query, (BIN,))
        banquet = cursor.fetchone()
        if not banquet:
            print("Banquet not found.")
            return

        # Update banquet details
        print("\nUpdate Banquet Details (leave the field empty if you don't want to change it).")
        Banquet_Name = input(f"Banquet Name ({banquet[1]}): ").strip() or banquet[1]

        while True:
            Date_input = input(f"Date ({banquet[2]} - YYYY-MM-DD): ").strip()
            if Date_input.lower() == 'exit.m':
                raise ExitToMainMenu
            elif Date_input.lower() == 'exit.p':
                raise ExitToPreviousSection
            if not Date_input:
                Date_input = banquet[2]
                break
            elif re.fullmatch(r'\d{4}-\d{2}-\d{2}', Date_input) and validate_date(Date_input):
                break
            else:
                print("Invalid date format. Please enter in YYYY-MM-DD format.")

        while True:
            Time_input = input(f"Time ({banquet[3]} - HH:MM:SS): ").strip()
            if Time_input.lower() == 'exit.m':
                raise ExitToMainMenu
            elif Time_input.lower() == 'exit.p':
                raise ExitToPreviousSection
            if not Time_input:
                Time_input = banquet[3]
                break
            elif re.fullmatch(r'\d{2}:\d{2}:\d{2}', Time_input) and validate_time(Time_input):
                break
            else:
                print("Invalid time format. Please enter in HH:MM:SS format.")

        Location = input(f"Location ({banquet[4]}): ").strip() or banquet[4]

        while True:
            Available = input(f"Available ({banquet[5]} - Y/N): ").strip().lower()
            if Available == 'exit.m':
                raise ExitToMainMenu
            elif Available == 'exit.p':
                raise ExitToPreviousSection
            if not Available:
                Available = banquet[5]
                break
            elif Available in ['y', 'n']:
                Available = Available.upper()
                break
            else:
                print("Invalid input. Please enter 'Y' or 'N' or type 'exit.m'/'exit.p' to navigate.")

        Quota = banquet[6]
        while True:
            Quota_input = input(f"Quota ({Quota}): ").strip()
            if Quota_input.lower() == 'exit.m':
                raise ExitToMainMenu
            elif Quota_input.lower() == 'exit.p':
                raise ExitToPreviousSection
            if not Quota_input:
                break
            try:
                quota_val = int(Quota_input)
                if quota_val < 1:
                    print("Quota must be at least 1.")
                    continue
                Quota = quota_val
                break
            except ValueError:
                print("Invalid input. Please enter a valid integer or type 'exit.m'/'exit.p' to navigate.")

        Address = input(f"Address ({banquet[7]}): ").strip() or banquet[7]
        Contact_First_Name = input(f"Contact Staff First Name ({banquet[8]}): ").strip() or banquet[8]
        Contact_Last_Name = input(f"Contact Staff Last Name ({banquet[9]}): ").strip() or banquet[9]

        # Insert updated details
        update_banquet_query = (
            "UPDATE New_banquet SET "
            "Banquet_Name=%s, Date=%s, Time=%s, Location=%s, Available=%s, Quota=%s, "
            "Address=%s, Contact_First_Name=%s, Contact_Last_Name=%s "
            "WHERE BIN=%s"
        )
        data = (Banquet_Name, Date_input, Time_input, Location, Available, Quota, Address, Contact_First_Name, Contact_Last_Name, BIN)
        cursor.execute(update_banquet_query, data)
        conn.commit()
        print("Banquet updated successfully.")
    except ExitToMainMenu:
        raise
    except ExitToPreviousSection:
        raise

def get_attendee_info():
    try:
        clear_terminal()
        print("\nGet Attendee Information")
        print("Exit Options: Type 'exit.m' to return to the Main Menu, 'exit.p' to return to the previous menu.")
        email = get_email_input("Enter attendee's email address: ")
        query = "SELECT * FROM Attendee WHERE Email_Address=%s"
        cursor.execute(query, (email,))
        attendee = cursor.fetchone()
        if attendee:
            print("\nAttendee Information:")
            columns = cursor.column_names
            attendee_info = dict(zip(columns, attendee))
            for key, value in attendee_info.items():
                print(f"{key}: {value}")

            # Update registration data fields if needed
            try:
                update = get_choice_input("Do you want to update attendee's information?", ['y', 'n'])
                if update == 'y':
                    # Use loops to validate input and allow re-entry
                    while True:
                        Address = input(f"Address ({attendee_info['Address']}): ").strip() or attendee_info['Address']
                        if Address.lower() == 'exit.m':
                            raise ExitToMainMenu
                        elif Address.lower() == 'exit.p':
                            raise ExitToPreviousSection
                        if Address:
                            break
                        else:
                            print("Address cannot be empty or type 'exit.m'/'exit.p' to navigate.")
                    while True:
                        Mobile_Number = input(f"Mobile Number ({attendee_info['Mobile_Number']}) (format: 8-digit number): ").strip() or attendee_info['Mobile_Number']
                        if Mobile_Number.lower() == 'exit.m':
                            raise ExitToMainMenu
                        elif Mobile_Number.lower() == 'exit.p':
                            raise ExitToPreviousSection
                        if re.fullmatch(r'\d{8}', Mobile_Number):
                            break
                        else:
                            print("Mobile Number must be an 8-digit number or type 'exit.m'/'exit.p' to navigate.")
                    update_query = (
                        "UPDATE Attendee SET Address=%s, Mobile_Number=%s WHERE Email_Address=%s"
                    )
                    cursor.execute(update_query, (Address, Mobile_Number, email))
                    conn.commit()
                    print("Attendee information updated.")
            except ExitToMainMenu:
                raise
            except ExitToPreviousSection:
                print("Returning to Administrator Menu.")
        else:
            print("Attendee not found.")
    except ExitToMainMenu:
        raise
    except ExitToPreviousSection:
        raise

def password_strength(password):
    """Assess the strength of a password and return a score out of 4."""
    score = 0

    if len(password) >= 8:
        score += 1
    if re.search(r'[A-Z]', password):
        score += 1
    if re.search(r'[a-z]', password):
        score += 1
    if re.search(r'[0-9]', password):
        score += 1

    return score

def display_password_strength(score):
    """Display a simple password strength bar."""
    total = 4
    bar_length = 10
    filled_length = int(bar_length * score / total)
    bar = '|' + '*' * filled_length + ' ' * (bar_length - filled_length) + '|'

    strength_levels = {
        0: "Very Weak",
        1: "Weak",
        2: "Moderate",
        3: "Strong",
        4: "Very Strong"
    }
    strength_message = strength_levels.get(score, "Unknown")

    print(f"Password Strength: {bar} {strength_message}")

def create_attendee_account():
    try:
        clear_terminal()
        print("\nCreate Attendee Account")
        print("Exit Options: Type 'exit.m' to return to the Main Menu, 'exit.p' to return to the previous menu.")

        # Collect First Name with validation
        First_Name = get_validated_input(
            "First Name: ",
            lambda x: x.isalpha(),
            "First Name must contain only English letters. Please try again or type 'exit.m'/'exit.p' to navigate."
        )

        # Collect Last Name with validation
        Last_Name = get_validated_input(
            "Last Name: ",
            lambda x: x.isalpha(),
            "Last Name must contain only English letters. Please try again or type 'exit.m'/'exit.p' to navigate."
        )

        # Collect Address
        Address = get_non_empty_string("Address: ")

        # Collect Attendee Type
        Attendee_Type = get_choice_input("Attendee Type", ['staff', 'student', 'alumni', 'guest'])

        # Collect Email Address in a loop, checking for duplicates
        while True:
            Email_Address = get_email_input("E-mail Address: ")

            # Check if the email already exists in the database
            check_email_query = "SELECT * FROM Attendee WHERE Email_Address=%s"
            cursor.execute(check_email_query, (Email_Address,))
            result = cursor.fetchone()

            if result:
                print("An account with this email already exists.")
                print("Please enter a different email or type 'exit.m' to return to the main menu, 'exit.p' to return to the previous menu.")
            else:
                break  # Email is unique, proceed

        # Password strength checking
        while True:
            Password = get_non_empty_string("Password (minimum 8 characters, include uppercase, lowercase, number): ")
            score = password_strength(Password)
            display_password_strength(score)
            if score < 4:
                print("Password is not strong enough. Please try again.")
            else:
                break

        # Collect Mobile Number
        Mobile_Number = get_mobile_number("Mobile Number: ")

        # Collect Affiliated Organization
        Affiliated_Organization = get_choice_input("Affiliated Organization", ['polyu', 'speed', 'hkcc', 'others']).upper()
        Affiliated_Organization = Affiliated_Organization if Affiliated_Organization != 'OTHERS' else 'Others'

        # Prepare the INSERT statement
        insert_attendee = (
            "INSERT INTO Attendee "
            "(First_Name, Last_Name, Address, Mobile_Number, Email_Address, Password, Attendee_Type, Affiliated_Organization) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        )
        attendee_data = (First_Name, Last_Name, Address, Mobile_Number, Email_Address, Password, Attendee_Type, Affiliated_Organization)

        try:
            # Attempt to insert the new attendee into the database
            cursor.execute(insert_attendee, attendee_data)
            conn.commit()
            print("Account created successfully.")
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_DUP_ENTRY:
                # This should not occur due to our prior check, but we handle it just in case
                print("An account with this email already exists. Please try signing up again.")
            else:
                print(err)
    except ExitToMainMenu:
        pass  # Return to Main Menu
    except ExitToPreviousSection:
        pass  # Return to Previous Section

def attendee_login(email, password):
    query = "SELECT * FROM Attendee WHERE Email_Address=%s AND Password=%s"
    cursor.execute(query, (email, password))
    attendee = cursor.fetchone()
    if attendee:
        print("Logged in successfully.")
        return attendee[0]  # Return Attendee_ID
    else:
        print("Invalid credentials.")
        return None

def update_attendee_profile(Attendee_ID):
    try:
        clear_terminal()
        print("\nUpdate Personal Information")
        print("Exit Options: Type 'exit.m' to return to the Main Menu, 'exit.p' to return to the previous menu.")
        query = "SELECT * FROM Attendee WHERE Attendee_ID=%s"
        cursor.execute(query, (Attendee_ID,))
        attendee = cursor.fetchone()
        if attendee:
            print("\nUpdate Profile Information (leave blank to keep current value):")
            columns = cursor.column_names
            attendee_info = dict(zip(columns, attendee))

            while True:
                Email_Address = input(f"E-mail Address ({attendee_info['Email_Address']}) (format: xxx@xxx.xxx): ").strip() or attendee_info['Email_Address']
                if Email_Address.lower() == 'exit.m':
                    raise ExitToMainMenu
                elif Email_Address.lower() == 'exit.p':
                    raise ExitToPreviousSection
                if re.fullmatch(r'^[\w\.-]+@[\w\.-]+\.\w+$', Email_Address):
                    break
                else:
                    print("Invalid email address. Please try again or type 'exit.m'/'exit.p' to navigate.")

            # Password strength checking
            while True:
                Password = input("Password (leave blank to keep current): ").strip()
                if Password.lower() == 'exit.m':
                    raise ExitToMainMenu
                elif Password.lower() == 'exit.p':
                    raise ExitToPreviousSection
                if not Password:
                    Password = attendee_info['Password']
                    break
                else:
                    score = password_strength(Password)
                    display_password_strength(score)
                    if score < 4:
                        print("Password is not strong enough. Please try again.")
                    else:
                        break

            while True:
                Mobile_Number = input(f"Mobile Number ({attendee_info['Mobile_Number']}) (format: 8-digit number): ").strip() or attendee_info['Mobile_Number']
                if Mobile_Number.lower() == 'exit.m':
                    raise ExitToMainMenu
                elif Mobile_Number.lower() == 'exit.p':
                    raise ExitToPreviousSection
                if re.fullmatch(r'\d{8}', Mobile_Number):
                    break
                else:
                    print("Mobile Number must be an 8-digit number. Please try again or type 'exit.m'/'exit.p' to navigate.")

            Address = input(f"Address ({attendee_info['Address']}): ").strip() or attendee_info['Address']
            if Address.lower() == 'exit.m':
                raise ExitToMainMenu
            elif Address.lower() == 'exit.p':
                raise ExitToPreviousSection

            # Update attendee information
            update_query = (
                "UPDATE Attendee SET Email_Address=%s, Password=%s, Mobile_Number=%s, Address=%s WHERE Attendee_ID=%s"
            )
            data = (Email_Address, Password, Mobile_Number, Address, Attendee_ID)
            cursor.execute(update_query, data)
            conn.commit()
            print("Profile updated successfully.")
        else:
            print("Attendee not found.")
    except ExitToMainMenu:
        raise
    except ExitToPreviousSection:
        raise

def register_for_banquet(Attendee_ID):
    try:
        clear_terminal()
        # List available banquets
        query = "SELECT * FROM New_banquet WHERE Available='Y'"
        cursor.execute(query)
        banquets = cursor.fetchall()
        if not banquets:
            print("No banquets available.")
            return
        print("\nBanquets:")
        for banquet in banquets:
            BIN = banquet[0]
            query_count = "SELECT COUNT(*) FROM Registration WHERE BIN=%s"
            cursor.execute(query_count, (BIN,))
            count = cursor.fetchone()[0]
            status = f"{count}/{banquet[6]}"  # banquet[6] is Quota
            if count >= banquet[6]:
                status += " (Full)"
            print(f"BIN: {banquet[0]}, Name: {banquet[1]}, Date: {banquet[2]}, Time: {banquet[3]}, "
                  f"Location: {banquet[4]}, Registered: {status}")

        BIN = get_integer_input("Enter BIN of the banquet to register: ", min_value=1)
        query = "SELECT * FROM New_banquet WHERE BIN=%s"
        cursor.execute(query, (BIN,))
        banquet = cursor.fetchone()
        if not banquet:
            print("Banquet not found.")
            return

        # Check if the banquet is full
        query_count = "SELECT COUNT(*) FROM Registration WHERE BIN=%s"
        cursor.execute(query_count, (BIN,))
        registered_count = cursor.fetchone()[0]
        if registered_count >= banquet[6]:  # Quota
            print("Sorry, the banquet is full.")
            return

        # Check if attendee already registered for this banquet
        query_check = "SELECT * FROM Registration WHERE BIN=%s AND Attendee_ID=%s"
        cursor.execute(query_check, (BIN, Attendee_ID))
        already_registered = cursor.fetchone()
        if already_registered:
            print("You have already registered for this banquet.")
            return

        # Register attendee
        Drink_Choice = get_choice_input("Drink Choice", ['tea', 'coffee', 'lemon tea'])

        # List available meals for the selected banquet
        query_meals = "SELECT Dish_Name FROM Meal WHERE BIN=%s"
        cursor.execute(query_meals, (BIN,))
        available_meals = [meal[0] for meal in cursor.fetchall()]
        if not available_meals:
            print("No meals available for this banquet.")
            return
        print("\nAvailable Meals:")
        for meal in available_meals:
            print(f"- {meal}")
        Meal_Choice = get_validated_input(
            "Meal Choice: ",
            lambda x: x in available_meals,
            "Invalid meal choice. Please select from the available meals or type 'exit.m' to return to the main menu, 'exit.p' to return to the previous menu."
        )

        Remarks = input("Remarks (e.g., seating preference) (optional): ").strip()
        if Remarks.lower() == 'exit.m':
            raise ExitToMainMenu
        elif Remarks.lower() == 'exit.p':
            raise ExitToPreviousSection

        Time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        Seat_No = registered_count + 1

        insert_registration = (
            "INSERT INTO Registration "
            "(Attendee_ID, BIN, Seat_No, Time, Meal_Choice, Drink_Choice, Remarks) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s)"
        )
        registration_data = (Attendee_ID, BIN, Seat_No, Time_now, Meal_Choice, Drink_Choice, Remarks if Remarks else None)
        cursor.execute(insert_registration, registration_data)
        conn.commit()
        print("Registered successfully for the banquet.")
    except ExitToMainMenu:
        raise
    except ExitToPreviousSection:
        raise

def search_registrations(Attendee_ID):
    try:
        clear_terminal()
        print("\nSearch Registrations:")
        print("Exit Options: Type 'exit.m' to return to the Main Menu, 'exit.p' to return to the previous menu.")
        print("1. By Date")
        print("2. By Banquet Name")
        while True:
            choice = input("Enter your choice (1/2): ").strip()
            if choice.lower() == 'exit.m':
                raise ExitToMainMenu
            elif choice.lower() == 'exit.p':
                raise ExitToPreviousSection
            if choice == '1':
                date = get_validated_input(
                    "Enter date (YYYY-MM-DD): ",
                    lambda x: re.fullmatch(r'\d{4}-\d{2}-\d{2}', x) is not None and validate_date(x),
                    "Invalid date format. Please enter in YYYY-MM-DD format."
                )
                query = (
                    "SELECT Registration.Registration_ID, New_banquet.Banquet_Name, New_banquet.Date, New_banquet.Time "
                    "FROM Registration "
                    "JOIN New_banquet ON Registration.BIN = New_banquet.BIN "
                    "WHERE Registration.Attendee_ID=%s AND New_banquet.Date=%s"
                )
                cursor.execute(query, (Attendee_ID, date))
                break
            elif choice == '2':
                name = get_non_empty_string("Enter part of banquet name: ")
                query = (
                    "SELECT Registration.Registration_ID, New_banquet.Banquet_Name, New_banquet.Date, New_banquet.Time "
                    "FROM Registration "
                    "JOIN New_banquet ON Registration.BIN = New_banquet.BIN "
                    "WHERE Registration.Attendee_ID=%s AND New_banquet.Banquet_Name LIKE %s"
                )
                cursor.execute(query, (Attendee_ID, f'%{name}%'))
                break
            else:
                print("Invalid choice. Please select 1 or 2 or type 'exit.m' to return to the main menu, 'exit.p' to return to the previous menu.")

        registrations = cursor.fetchall()
        if registrations:
            print("\nYour Registrations:")
            for reg in registrations:
                print(f"Registration_ID: {reg[0]}, Banquet Name: {reg[1]}, Date: {reg[2]}, Time: {reg[3]}")
        else:
            print("No registrations found.")
    except ExitToMainMenu:
        raise
    except ExitToPreviousSection:
        raise

def update_registration(Attendee_ID):
    try:
        clear_terminal()
        print("\nUpdate Registration")
        print("Exit Options: Type 'exit.m' to return to the Main Menu, 'exit.p' to return to the previous menu.")
        Registration_ID = get_integer_input("Enter Registration ID to update: ", min_value=1)
        query = "SELECT * FROM Registration WHERE Registration_ID=%s AND Attendee_ID=%s"
        cursor.execute(query, (Registration_ID, Attendee_ID))
        registration = cursor.fetchone()
        if not registration:
            print("Registration not found.")
            return

        print("\nUpdate Registration Details (leave the field empty if you don't want to change it).")

        Meal_Choice = input(f"Meal Choice ({registration[5]}): ").strip()
        if Meal_Choice.lower() == 'exit.m':
            raise ExitToMainMenu
        elif Meal_Choice.lower() == 'exit.p':
            raise ExitToPreviousSection
        if not Meal_Choice:
            Meal_Choice = registration[5]
        else:
            # Verify that the meal exists for the banquet
            BIN = registration[2]
            query_meals = "SELECT Dish_Name FROM Meal WHERE BIN=%s"
            cursor.execute(query_meals, (BIN,))
            available_meals = [meal[0] for meal in cursor.fetchall()]
            if Meal_Choice not in available_meals:
                print("Invalid meal choice.")
                return

        Drink_Choice = input(f"Drink Choice ({registration[6]} - tea/coffee/lemon tea): ").strip().lower()
        if Drink_Choice.lower() == 'exit.m':
            raise ExitToMainMenu
        elif Drink_Choice.lower() == 'exit.p':
            raise ExitToPreviousSection
        if not Drink_Choice:
            Drink_Choice = registration[6]
        elif Drink_Choice not in ['tea', 'coffee', 'lemon tea']:
            print("Invalid drink choice.")
            return

        Remarks = input(f"Remarks ({registration[7]}): ").strip()
        if Remarks.lower() == 'exit.m':
            raise ExitToMainMenu
        elif Remarks.lower() == 'exit.p':
            raise ExitToPreviousSection
        Remarks = Remarks or registration[7]

        update_query = (
            "UPDATE Registration SET Meal_Choice=%s, Drink_Choice=%s, Remarks=%s WHERE Registration_ID=%s"
        )
        cursor.execute(update_query, (Meal_Choice, Drink_Choice, Remarks, Registration_ID))
        conn.commit()
        print("Registration updated successfully.")
    except ExitToMainMenu:
        raise
    except ExitToPreviousSection:
        raise

def generate_reports():
    try:
        while True:
            clear_terminal()
            print("\nReport Generation:")
            print("Exit Options: Type 'exit.m' to return to the Main Menu, 'exit.p' to return to the previous menu.")
            print("1. Registration Status Report")
            print("2. Popular Meals Report")
            print("3. Attendee Behavior Report")
            print("4. Banquet Popularity Report")
            print("5. Attendee Demographics Report")
            print("6. Generate All Reports")
            print("7. Back to Administrator Menu")
            choice = input("Enter your choice: ").strip()
            if choice.lower() == 'exit.m':
                raise ExitToMainMenu
            elif choice.lower() == 'exit.p':
                raise ExitToPreviousSection
            if choice == '1':
                generate_registration_status_report()
            elif choice == '2':
                generate_popular_meals_report()
            elif choice == '3':
                generate_attendee_behavior_report()
            elif choice == '4':
                generate_banquet_popularity_report()
            elif choice == '5':
                generate_attendee_demographics_report()
            elif choice == '6':
                generate_registration_status_report()
                generate_popular_meals_report()
                generate_attendee_behavior_report()
                generate_banquet_popularity_report()
                generate_attendee_demographics_report()
                print("\nAll reports have been generated.")
            elif choice == '7':
                print("Returning to Administrator Menu.")
                break
            else:
                print("Invalid choice. Please select from 1 to 7 or type 'exit.m'/'exit.p' to navigate.")
            input("Press Enter to continue...")
    except ExitToMainMenu:
        raise
    except ExitToPreviousSection:
        raise

def generate_registration_status_report():
    # Registration Status Report
    print("\nGenerating Registration Status Report...")
    query = (
        "SELECT New_banquet.BIN, New_banquet.Banquet_Name, New_banquet.Quota, "
        "COUNT(Registration.Registration_ID) as Registered, "
        "ROUND((COUNT(Registration.Registration_ID)/New_banquet.Quota)*100, 2) AS Fill_Percentage "
        "FROM New_banquet "
        "LEFT JOIN Registration ON New_banquet.BIN = Registration.BIN "
        "GROUP BY New_banquet.BIN "
        "ORDER BY New_banquet.Date, New_banquet.Time"
    )
    cursor.execute(query)
    report = cursor.fetchall()

    # Prepare the report content
    report_lines = []
    report_lines.append("--------------------------------------------------")
    report_lines.append("                 Registration Status Report")
    report_lines.append("--------------------------------------------------")
    if report:
        for row in report:
            BIN = row[0]
            name = row[1]
            quota = row[2]
            registered = row[3]
            fill_percentage = row[4]
            status = "Full" if registered >= quota else "Open"
            report_lines.append(f"BIN: {BIN}")
            report_lines.append(f"Banquet Name: {name}")
            report_lines.append(f"Quota: {quota}")
            report_lines.append(f"Registered: {registered} ({fill_percentage}%) - Status: {status}")
            report_lines.append("--------------------------------------------------")
    else:
        report_lines.append("No registration data available.")
        report_lines.append("--------------------------------------------------")

    # Add recommendations
    report_lines.append("\nRecommendations:")
    report_lines.append("- Monitor banquets approaching full capacity and consider increasing quotas if feasible.")
    report_lines.append("- For banquets with low registration, implement promotional activities.")
    report_lines.append("--------------------------------------------------")

    report_content = "\n".join(report_lines)

    # Write to txt file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    report_path = os.path.join(script_dir, 'registration_status_report.txt')
    with open(report_path, 'w') as report_file:
        report_file.write(report_content)
    print(f"Registration Status Report has been generated at {report_path}")

def generate_popular_meals_report():
    # Popular Meals Report
    print("\nGenerating Popular Meals Report...")
    query = (
        "SELECT Meal_Choice, COUNT(*) as Count "
        "FROM Registration "
        "GROUP BY Meal_Choice "
        "ORDER BY Count DESC"
    )
    cursor.execute(query)
    report = cursor.fetchall()

    # Prepare the report content
    report_lines = []
    report_lines.append("--------------------------------------------------")
    report_lines.append("                 Popular Meals Report")
    report_lines.append("--------------------------------------------------")
    if report:
        total_selections = sum([row[1] for row in report])
        for row in report:
            meal = row[0]
            count = row[1]
            percentage = (count / total_selections) * 100 if total_selections > 0 else 0
            report_lines.append(f"Meal: {meal}")
            report_lines.append(f"Number of Selections: {count} ({percentage:.2f}%)")
            report_lines.append("--------------------------------------------------")
    else:
        report_lines.append("No meal selection data available.")
        report_lines.append("--------------------------------------------------")

    # Add recommendations
    report_lines.append("\nRecommendations:")
    report_lines.append("- Consider featuring the most popular meals in future banquets.")
    report_lines.append("- Analyze less popular meals to determine if they should be replaced or improved.")
    report_lines.append("--------------------------------------------------")

    report_content = "\n".join(report_lines)

    # Write to txt file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    report_path = os.path.join(script_dir, 'popular_meals_report.txt')
    with open(report_path, 'w') as report_file:
        report_file.write(report_content)
    print(f"Popular Meals Report has been generated at {report_path}")

def generate_attendee_behavior_report():
    # Attendee Behavior Report
    print("\nGenerating Attendee Behavior Report...")
    query = (
        "SELECT Attendee.Attendee_ID, Attendee.First_Name, Attendee.Last_Name, "
        "COUNT(Registration.Registration_ID) AS Total_Registrations, "
        "GROUP_CONCAT(DISTINCT New_banquet.Banquet_Name SEPARATOR ', ') AS Banquets_Attended, "
        "GROUP_CONCAT(DISTINCT Meal_Choice SEPARATOR ', ') AS Meals_Chosen "
        "FROM Attendee "
        "LEFT JOIN Registration ON Attendee.Attendee_ID = Registration.Attendee_ID "
        "LEFT JOIN New_banquet ON Registration.BIN = New_banquet.BIN "
        "GROUP BY Attendee.Attendee_ID "
        "ORDER BY Total_Registrations DESC"
    )
    cursor.execute(query)
    report = cursor.fetchall()

    # Prepare the report content
    report_lines = []
    report_lines.append("--------------------------------------------------")
    report_lines.append("                 Attendee Behavior Report")
    report_lines.append("--------------------------------------------------")
    if report:
        for row in report:
            attendee_id = row[0]
            name = f"{row[1]} {row[2]}"
            total_regs = row[3]
            banquets = row[4] if row[4] else 'None'
            meals = row[5] if row[5] else 'None'
            report_lines.append(f"Attendee ID: {attendee_id}")
            report_lines.append(f"Name: {name}")
            report_lines.append(f"Total Registrations: {total_regs}")
            report_lines.append(f"Banquets Attended: {banquets}")
            report_lines.append(f"Meals Chosen: {meals}")
            report_lines.append("--------------------------------------------------")
    else:
        report_lines.append("No attendee data available.")
        report_lines.append("--------------------------------------------------")

    # Add recommendations
    report_lines.append("\nRecommendations:")
    report_lines.append("- Identify highly engaged attendees for loyalty programs.")
    report_lines.append("- Analyze meal preferences to tailor future menus.")
    report_lines.append("--------------------------------------------------")

    report_content = "\n".join(report_lines)

    # Write to txt file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    report_path = os.path.join(script_dir, 'attendee_behavior_report.txt')
    with open(report_path, 'w') as report_file:
        report_file.write(report_content)
    print(f"Attendee Behavior Report has been generated at {report_path}")

def generate_banquet_popularity_report():
    # Banquet Popularity Report
    print("\nGenerating Banquet Popularity Report...")
    query = (
        "SELECT New_banquet.BIN, New_banquet.Banquet_Name, New_banquet.Quota, "
        "COUNT(Registration.Registration_ID) as Registered, "
        "ROUND((COUNT(Registration.Registration_ID)/New_banquet.Quota)*100, 2) AS Fill_Percentage "
        "FROM New_banquet "
        "LEFT JOIN Registration ON New_banquet.BIN = Registration.BIN "
        "GROUP BY New_banquet.BIN "
        "ORDER BY Registered DESC"
    )
    cursor.execute(query)
    report = cursor.fetchall()

    # Prepare the report content
    report_lines = []
    report_lines.append("--------------------------------------------------")
    report_lines.append("                 Banquet Popularity Report")
    report_lines.append("--------------------------------------------------")
    if report:
        for row in report:
            BIN = row[0]
            name = row[1]
            quota = row[2]
            registered = row[3]
            fill_percentage = row[4]
            status = "Full" if registered >= quota else "Open"
            report_lines.append(f"BIN: {BIN}")
            report_lines.append(f"Name: {name}")
            report_lines.append(f"Quota: {quota}")
            report_lines.append(f"Registered: {registered} ({fill_percentage}%) - {status}")
            report_lines.append("--------------------------------------------------")
    else:
        report_lines.append("No banquet data available.")
        report_lines.append("--------------------------------------------------")

    # Add recommendations
    report_lines.append("\nRecommendations:")
    report_lines.append("- For banquets with high demand, consider increasing the quota.")
    report_lines.append("- Promote banquets with low registration to boost attendance.")
    report_lines.append("--------------------------------------------------")

    report_content = "\n".join(report_lines)

    # Write to txt file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    report_path = os.path.join(script_dir, 'banquet_popularity_report.txt')
    with open(report_path, 'w') as report_file:
        report_file.write(report_content)
    print(f"Banquet Popularity Report has been generated at {report_path}")

def generate_attendee_demographics_report():
    # Attendee Demographics Report
    print("\nGenerating Attendee Demographics Report...")
    query = (
        "SELECT Attendee_Type, COUNT(*) AS Count "
        "FROM Attendee "
        "GROUP BY Attendee_Type"
    )
    cursor.execute(query)
    attendee_types = cursor.fetchall()

    query = (
        "SELECT Affiliated_Organization, COUNT(*) AS Count "
        "FROM Attendee "
        "GROUP BY Affiliated_Organization"
    )
    cursor.execute(query)
    affiliated_orgs = cursor.fetchall()

    # Prepare the report content
    report_lines = []
    report_lines.append("--------------------------------------------------")
    report_lines.append("                 Attendee Demographics Report")
    report_lines.append("--------------------------------------------------")
    report_lines.append("\nAttendee Types:")
    total_attendees = sum([row[1] for row in attendee_types])
    for row in attendee_types:
        attendee_type = row[0]
        count = row[1]
        percentage = (count / total_attendees) * 100 if total_attendees > 0 else 0
        report_lines.append(f"- {attendee_type.capitalize()}: {count} ({percentage:.2f}%)")
    report_lines.append("\nAffiliated Organizations:")
    total_attendees = sum([row[1] for row in affiliated_orgs])
    for row in affiliated_orgs:
        org = row[0]
        count = row[1]
        percentage = (count / total_attendees) * 100 if total_attendees > 0 else 0
        report_lines.append(f"- {org}: {count} ({percentage:.2f}%)")
    report_lines.append("--------------------------------------------------")

    # Add recommendations
    report_lines.append("\nRecommendations:")
    report_lines.append("- Target underrepresented attendee types in future promotions.")
    report_lines.append("- Partner with affiliated organizations to increase engagement.")
    report_lines.append("--------------------------------------------------")

    report_content = "\n".join(report_lines)

    # Write to txt file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    report_path = os.path.join(script_dir, 'attendee_demographics_report.txt')
    with open(report_path, 'w') as report_file:
        report_file.write(report_content)
    print(f"Attendee Demographics Report has been generated at {report_path}")

def create_admin_account():
    try:
        clear_terminal()
        print("\nCreate Administrator Account")
        print("Exit Options: Type 'exit.m' to return to the Main Menu, 'exit.p' to return to the previous menu.")
        First_Name = get_validated_input(
            "First Name: ",
            lambda x: x.isalpha(),
            "First Name must contain only English letters. Please try again or type 'exit.m'/'exit.p' to navigate."
        )

        Last_Name = get_validated_input(
            "Last Name: ",
            lambda x: x.isalpha(),
            "Last Name must contain only English letters. Please try again or type 'exit.m'/'exit.p' to navigate."
        )

        Address = get_non_empty_string("Address: ")

        Email_Address = get_email_input("E-mail Address: ")

        # Password strength checking
        while True:
            Password = get_non_empty_string("Password (minimum 8 characters, include uppercase, lowercase, number): ")
            score = password_strength(Password)
            display_password_strength(score)
            if score < 4:
                print("Password is not strong enough. Please try again.")
            else:
                break

        Mobile_Number = get_mobile_number("Mobile Number: ")

        insert_admin = (
            "INSERT INTO Administrator "
            "(First_Name, Last_Name, Address, Mobile_Number, Email_Address, Password) "
            "VALUES (%s, %s, %s, %s, %s, %s)"
        )
        admin_data = (First_Name, Last_Name, Address, Mobile_Number, Email_Address, Password)
        try:
            cursor.execute(insert_admin, admin_data)
            conn.commit()
            print("Administrator account created successfully.")
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_DUP_ENTRY:
                print("An account with this email already exists.")
            else:
                print(err)
    except ExitToMainMenu:
        raise
    except ExitToPreviousSection:
        raise

def main_menu():
    while True:
        try:
            clear_terminal()
            print("\nBanquet Management System")
            print("Exit Options: Type 'exit.m' to return to the Main Menu.")
            print("1. Administrator Login")
            print("2. Create Administrator Account")
            print("3. Attendee Sign Up")
            print("4. Attendee Login")
            print("5. Exit")
            choice = input("Enter your choice (1-5): ").strip()

            if choice.lower() == 'exit.m':
                print("You are already at the Main Menu.")
                continue
            elif choice.lower() == 'exit.p':
                print("You are already at the Main Menu.")
                continue

            if choice == '1':
                try:
                    email = get_email_input("Email Address: ")
                    password = get_non_empty_string("Password: ")
                    admin_id = admin_login(email, password)
                    if admin_id:
                        administrator_menu(admin_id)
                except ExitToMainMenu:
                    continue
                except ExitToPreviousSection:
                    print("Returning to Main Menu.")
            elif choice == '2':
                try:
                    create_admin_account()
                except ExitToMainMenu:
                    continue
                except ExitToPreviousSection:
                    print("Returning to Main Menu.")
            elif choice == '3':
                try:
                    create_attendee_account()
                except ExitToMainMenu:
                    continue
                except ExitToPreviousSection:
                    print("Returning to Main Menu.")
            elif choice == '4':
                try:
                    email = get_email_input("Email Address: ")
                    password = get_non_empty_string("Password: ")
                    attendee_id = attendee_login(email, password)
                    if attendee_id:
                        attendee_menu(attendee_id)
                except ExitToMainMenu:
                    continue
                except ExitToPreviousSection:
                    print("Returning to Main Menu.")
            elif choice == '5':
                print("Exiting the system.")
                break
            else:
                print("Invalid choice. Please select from 1 to 5 or type 'exit.m'/'exit.p' to navigate.")
        except ExitToMainMenu:
            continue
        except ExitToPreviousSection:
            print("You are already at the Main Menu.")

    # Close the connection
    cursor.close()
    conn.close()

def administrator_menu(admin_id):
    while True:
        try:
            clear_terminal()
            print("\nAdministrator Menu")
            print("Exit Options: Type 'exit.m' to return to the Main Menu.")
            print("1. Create a New Banquet")
            print("2. Update Existing Banquet")
            print("3. Get Attendee Information")
            print("4. Generate Reports")
            print("5. Logout")
            admin_choice = input("Enter your choice (1-5): ").strip()
            if admin_choice.lower() == 'exit.m':
                raise ExitToMainMenu
            elif admin_choice.lower() == 'exit.p':
                print("Already in the Administrator Menu. Cannot go back further.")
                continue
            if admin_choice == '1':
                create_banquet()
            elif admin_choice == '2':
                update_banquet()
            elif admin_choice == '3':
                get_attendee_info()
            elif admin_choice == '4':
                generate_reports()
            elif admin_choice == '5':
                print("Logging out from Administrator account.")
                break
            else:
                print("Invalid choice. Please select from 1 to 5 or type 'exit.m'/'exit.p' to navigate.")
        except ExitToMainMenu:
            raise
        except ExitToPreviousSection:
            print("Already in the Administrator Menu. Cannot go back further.")

def attendee_menu(attendee_id):
    while True:
        try:
            clear_terminal()
            print("\nAttendee Menu")
            print("Exit Options: Type 'exit.m' to return to the Main Menu.")
            print("1. Update Personal Information")
            print("2. Register for a Banquet")
            print("3. Search Registrations")
            print("4. Update Registration")
            print("5. Logout")
            attendee_choice = input("Enter your choice (1-5): ").strip()
            if attendee_choice.lower() == 'exit.m':
                raise ExitToMainMenu
            elif attendee_choice.lower() == 'exit.p':
                print("Already in the Attendee Menu. Cannot go back further.")
                continue
            if attendee_choice == '1':
                update_attendee_profile(attendee_id)
            elif attendee_choice == '2':
                register_for_banquet(attendee_id)
            elif attendee_choice == '3':
                search_registrations(attendee_id)
            elif attendee_choice == '4':
                update_registration(attendee_id)
            elif attendee_choice == '5':
                print("Logging out from Attendee account.")
                break
            else:
                print("Invalid choice. Please select from 1 to 5 or type 'exit.m'/'exit.p' to navigate.")
        except ExitToMainMenu:
            raise
        except ExitToPreviousSection:
            print("Already in the Attendee Menu. Cannot go back further.")

def main():
    create_tables()
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\nExiting the system.")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
    finally:
        try:
            cursor.close()
            conn.close()
        except:
            pass

if __name__ == "__main__":
    main()