import sqlite3
import datetime

DB_NAME = 'serpent.db'

# TODO: Finish adding fields to configuration tables
CREATE_TABLE_COMMAND = """
    CREATE TABLE IF NOT EXISTS operations(
        id INTEGER PRIMARY KEY,
        op_name TEXT NOT NULL,
        is_current BOOLEAN NOT NULL,
        creation_date DATE NOT NULL
    );

    CREATE TABLE IF NOT EXISTS targets(
        id INTEGER PRIMARY KEY,
        ip TEXT,
        hostname TEXT,
        os TEXT,
        ops_notes TEXT
    );

    CREATE TABLE IF NOT EXISTS payload_configurations(
        id INTEGER PRIMARY KEY,
        op INTEGER NOT NULL,
        FOREIGN KEY(op) REFERENCES operations(id)
    );

    CREATE TABLE IF NOT EXISTS agent_configurations(
        callback_token TEXT PRIMARY KEY,
        op INTEGER NOT NULL,
        target_id INTEGER NOT NULL,
        callback_port INTEGER NOT NULL,
        listener_type TEXT NOT NULL,
        FOREIGN KEY(op) REFERENCES operations(id),
        FOREIGN KEY(target_id) REFERENCES targets(id)
    );

    CREATE TABLE IF NOT EXISTS port_scan_results(
        id INTEGER PRIMARY KEY,
        op INTEGER NOT NULL,
        target_id ID NOT NULL,
        port INTEGER NOT NULL,
        status TEXT NOT NULL,
        scan_time DATE NOT NULL,
        FOREIGN KEY(op) REFERENCES operations(id),
        FOREIGN KEY(target_id) REFERENCES targets(id)
    );
"""

def convert_results_to_string(results_list):
    return '\n'.join(
        [
            ', '.join(
                [
                    str(item) for item in result_tuple
                ]
            )
            
            for result_tuple in results_list
        ]
    )

def execute_command(command):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.executescript(command)
    conn.commit()
    conn.close()

def execute_query(query):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(query)
    results = c.fetchall()
    conn.commit()
    conn.close()

    return results

# TODO: Implement support for schema changes
def create_db_tables_if_not_exists():
    execute_command(CREATE_TABLE_COMMAND)

def get_all_ops():
    return execute_query("SELECT * FROM operations")

def get_current_op():
    current_op_results = execute_query("SELECT * FROM operations WHERE is_current = 1")
    if len(current_op_results) == 0:
        return None
    elif len(current_op_results) == 1:
        return current_op_results[0]
    else:
        raise Exception("ERROR: Multiple operations marked as current in the database (should only be one that is marked as current)")

def get_op(op_name):
    return execute_query("SELECT * FROM operations WHERE op_name = '%s'" % op_name)

def start_op(op_name):
    rows_for_op_name = get_op(op_name)
    if len(rows_for_op_name) != 0:
        print("Cannot start op with name of '%s'; operation with that name already exists" % op_nam)
        return

    execute_command("INSERT INTO operations (op_name, is_current, creation_date) VALUES ('%s', 1, '%s')" % (op_name, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

def store_scan_results(results):
    pass

def query_table(table_name, params):
    pass

def query_targets(params):
    pass

def query_agents(params):
    pass

def record_agent_callback_configuration(op_id, target_id, callback_token, callback_port, listener_type):
    command = """
        INSERT INTO agent_configurations (op_id, target_id, callback_token, callback_port, listener_type) VALUES (%s, %s, %s, %s, %s);
    """ % (op_id, target_id, callback_token, callback_port, listener_type)
    
    execute_command(command)
