from sqlite3 import *

from string import ascii_uppercase, ascii_lowercase, digits
from random import choices
from object.debug import log

class Database():
    """
    The accounts database.
    Store the phone number, the name, the last name and the age of a person.
    Assign a unique id for each account.
    """

    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        """
        Create the accounts' table.
        """

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS accounts(
                            account_id TEXT,
                            phone_number TEXT,
                            name TEXT,
                            lastname TEXT,
                            age INTEGER)""")
        self.conn.commit()
        log("Accounts table created!")

    def get_account_by_phone(self, phone_number: str) -> dict:
        """
        Get an account from the database, thanks to the phone_number.

        Args:
            phone_number (str): the phone number of the account
        
        Returns:
            dict: the account
        """

        self.cursor.execute("SELECT * FROM accounts WHERE phone_number=?", (phone_number,))
        return self.cursor.fetchone()

    def get_account_by_id(self, account_id: str) -> dict:
        """
        Get an account from the database, thanks to the account_id.

        Args:
            account_id (str): the account id of the account
        
        Returns:
            dict: the account
        """

        self.cursor.execute("SELECT * FROM accounts WHERE account_id=?", (account_id,))
        return self.cursor.fetchone()

    def create_account(self, phone_number: str, name: str, last_name: str, age: int):
        """
        Add an account to the database.

        Args:
            phone_number (str): the phone number of the user
            name (str): the name of the user
            last_name (str): the last name of the user
            age (int): the age of the user
        """
        
        characters = ascii_lowercase + ascii_uppercase + digits
        account_id = "".join(choices(characters, k=16))
        
        while self.get_account_by_id(account_id) is not None:
            account_id = "".join(choices(characters, k=16))

        self.cursor.execute("INSERT INTO accounts VALUES (?, ?, ?, ?, ?)", (account_id, phone_number, name, last_name, age))
        self.conn.commit()
        log(f"Account created with the phone number: {phone_number}")
