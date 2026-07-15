import os
import sqlite3
import pandas as pd

DB_PATH = "db/nifty100.db"

OUTPUT_DIR = "output"

os.makedirs(OUTPUT_DIR, exist_ok=True)