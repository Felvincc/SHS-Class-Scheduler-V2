import sqlite3
import CLI

connect = sqlite3.connect('data.db')

c = connect.cursor()

CLI()

