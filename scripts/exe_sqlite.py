#!/usr/bin/env python

""" Run a SQLite script """

from pathlib import Path
import re
import sqlite3
import sys



# con = sqlite3.connect("tutorial.db")
# cur = con.cursor()
# cur.execute("CREATE TABLE movie(title, year, score)")

def run_script(db_file: Path):
    # read commands
    f = sys.stdin.read()
    commands = re.split(r';\s*(?=\n|$)', f, maxsplit=0, flags=re.DOTALL)
    commands = [cmd.strip() + ';' for cmd in commands if cmd.strip()]
    if not commands:
        print("empty cmd list", file=sys.stderr)
        return

    # open connection
    con = sqlite3.connect(db_file)

    # execute commands
    for command in commands:
        print(command)
        try:
            with con:
                result = con.execute(command)
            print(result)
        except Exception as e:
            print(f"Error: {str(e)}")

    # close the connection
    con.close


def main():
    """Main logic"""
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <db_filename.db>")
        sys.exit(1)

    db_file = Path(sys.argv[1])
    if not db_file.exists():
        print(f"Error: File {db_file} not found")
        sys.exit(1)
    
    run_script(db_file)
    print(f"Done creating {db_file}")


if __name__ == '__main__':
    main()


