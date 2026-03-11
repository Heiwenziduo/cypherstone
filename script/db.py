import sqlite3

class KeyDatabase:
    def __init__(self, db_name):
        # This creates the file if it doesn't exist
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        # Create a table to store our keys and marks
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS key_pairs (
                alias TEXT,
                fingerprint TEXT,
                private_key BLOB,
                public_key BLOB,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expired_at TIMESTAMP,
                PRIMARY KEY (fingerprint)
            )
        ''')
        self.conn.commit()

    def save_key(self, alias, fingerprint, priv_bytes, pub_bytes):
        # Using 'REPLACE' makes it easy to update an existing alias
        query = "REPLACE INTO key_pairs (alias, fingerprint, private_key, public_key) VALUES (?, ?, ?, ?)"
        self.cursor.execute(query, (alias, fingerprint, priv_bytes, pub_bytes))
        self.conn.commit()

    def get_key_by_alias(self, alias):
        query = "SELECT private_key FROM key_pairs WHERE alias = ?"
        self.cursor.execute(query, (alias,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def get_row_by_fp(self, fp):
        query = "SELECT * FROM key_pairs WHERE fingerprint LIKE ?"
        '''
        When you only have the beginning of a string, you use the LIKE operator combined with a wildcard symbol (%).
        The % acts as a "filler" for whatever comes after your 12 characters.
        '''
        self.cursor.execute(query, (f"{fp}%",))
        result = self.cursor.fetchone()
        # print(result) # row
        return result if result else None

    def list_all_aliases(self):
        self.cursor.execute("SELECT alias FROM key_pairs")
        # print("fetch all", self.cursor.fetchall()) # consumable, once used, cursor changed
        return [row[0] for row in self.cursor.fetchall()]

    def list_all_table_data(self):
        self.cursor.execute("SELECT alias, fingerprint, private_key FROM key_pairs")
        # print("fetch all", self.cursor.fetchall())
        # for row in self.cursor.fetchall():
        #     print("row", row)
        return [(row[1][:12], row[0], "pair" if row[2] != None else "public-only") for row in self.cursor.fetchall()]
