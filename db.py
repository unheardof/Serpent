import sqlite3
import datetime

DB_NAME = 'serpent.db'

CREATE_TABLE_COMMANDS = [
    """
    CREATE TABLE IF NOT EXISTS operations(
        id INTEGER AUTOINCREMENTING PRIMARY KEY,
        op_name TEXT NOT NULL,
        is_current BOOLEAN NOT NULL,
        creation_date DATE NOT NULL
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS agents(
        id INTEGER AUTOINCREMENTING PRIMARY KEY,
        op INTEGER NOT NULL,
        configuration INTEGER NOT NULL,
        FOREIGN KEY(op) REFERENCES operations(id),
        FOREIGN KEY(configuration) REFERENCES agent_configurations(id)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS listeners(
        id INTEGER AUTOINCREMENTING PRIMARY KEY,
        op INTEGER NOT NULL,
        configuration INTEGER NOT NULL,
        FOREIGN KEY(op) REFERENCES operations(id),
        FOREIGN KEY(configuration) REFERENCES listener_configurations(id)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS targets(
        id INTEGER AUTOINCREMENTING PRIMARY KEY,
        ip TEXT,
        hostname TEXT,
        os TEXT,
        ops_notes TEXT
    );
    """,

    # TODO: Finish adding fields
    """
    CREATE TABLE IF NOT EXISTS payload_configurations(
        id INTEGER AUTOINCREMENTING PRIMARY KEY,
        op INTEGER NOT NULL,
        FOREIGN KEY(op) REFERENCES operations(id)
    );
    """,

    # TODO: Finish adding fields
    """
    CREATE TABLE IF NOT EXISTS listener_configurations(
        id INTEGER AUTOINCREMENTING,
        op INTEGER NOT NULL,
        FOREIGN KEY(op) REFERENCES operations(id)
    );
    """,

    # TODO: Finish adding fields
    """
    CREATE TABLE IF NOT EXISTS agent_configurations(
        id INTEGER AUTOINCREMENTING PRIMARY KEY,
        op INTEGER NOT NULL,
        target_id INTEGER NOT NULL,
        FOREIGN KEY(op) REFERENCES operations(id),
        FOREIGN KEY(target_id) REFERENCES targets(id)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS port_scan_results(
        id INTEGER AUTOINCREMENTING PRIMARY KEY,
        op INTEGER NOT NULL,
        target_id ID NOT NULL,
        port INTEGER NOT NULL,
        status TEXT NOT NULL,
        scan_time DATE NOT NULL,
        FOREIGN KEY(op) REFERENCES operations(id),
        FOREIGN KEY(target_id) REFERENCES targets(id)
    );
    """
]


def execute_commands(commands):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    for command in commands:
        c.execute(command)
        
    conn.commit()
    conn.close()

# TODO: Implement support for schema changes
def create_db_tables_if_not_exists():
    execute_commands(CREATE_TABLE_COMMANDS)

def start_op(op_name):
    
    execute_commands(["INSERT INTO operations (op_name, is_current, creation_date) VALUES (%s, 1, %s)" % (op_name, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))])

def store_scan_results(results):
    pass

def query_table(table_name, params):
    pass

def query_targets(params):
    pass

def query_agents(params):
    pass

