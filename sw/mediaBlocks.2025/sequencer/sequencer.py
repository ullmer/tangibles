# Original code by Brygg Ullmer, John Alex, et al., MIT Media Lab, 1998
# Port co-lead by CoPilot 2025
# Begun 2025-06-08

import yaml
import sqlite3

class Sequencer:
    def __init__(self, config_path, db_path):
        self.config = self.load_config(config_path)
        self.db_path = db_path
        self.setup_database()

    def load_config(self, path):
        with open(path, 'r') as file:
            return yaml.safe_load(file)

    def setup_database(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sequences (
                id INTEGER PRIMARY KEY,
                name TEXT,
                length INTEGER
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sequence_items (
                id INTEGER PRIMARY KEY,
                sequence_id INTEGER,
                item_name TEXT,
                FOREIGN KEY(sequence_id) REFERENCES sequences(id)
            )
        ''')
        conn.commit()
        conn.close()

    def create_sequence(self, name, length, items):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO sequences (name, length) VALUES (?, ?)', (name, length))
        sequence_id = cursor.lastrowid
        for item in items:
            cursor.execute('INSERT INTO sequence_items (sequence_id, item_name) VALUES (?, ?)', (sequence_id, item))
        conn.commit()
        conn.close()

    def get_sequences(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM sequences')
        sequences = cursor.fetchall()
        conn.close()
        return sequences

    def get_sequence_items(self, sequence_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM sequence_items WHERE sequence_id = ?', (sequence_id,))
        items = cursor.fetchall()
        conn.close()
        return items
