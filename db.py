import sqlite3

DB_NAME = 'serpent'

CREATE_SERPENT_DB_TABLES_COMMAND = """
    CREATE TABLE IF NOT EXISTS operations(
        id INTEGER AUTOINCREMENTING PRIMARY KEY,
        op_name TEXT NOT NULL,
        is_current BOOLEAN NOT NULL,
        creation_date DATE NOT NULL,
    );
    
    CREATE TABLE IF NOT EXISTS agents(
        id INTEGER AUTOINCREMENTING PRIMARY KEY,
        op INTEGER NOT NULL,
        configuration INTEGER NOT NULL,
        FOREIGN KEY(op) REFERENCES operations(id),
        FOREIGN KEY(configuration) REFERENCES agent_configurations(id)
    );
    
    CREATE TABLE IF NOT EXISTS listeners(
        id INTEGER AUTOINCREMENTING PRIMARY KEY,
        op INTEGER NOT NULL,
        configuration INTEGER NOT NULL,
        FOREIGN KEY(op) REFERENCES operations(id),
        FOREIGN KEY(configuration) REFERENCES listener_configurations(id)
    );
    
    CREATE TABLE IF NOT EXISTS targets(
        id INTEGER AUTOINCREMENTING PRIMARY KEY,
        ip TEXT,
        hostname TEXT,
        os TEXT,
        ops_notes TEXT
    );
    
    # TODO: Finish adding fields
    CREATE TABLE IF NOT EXISTS payload_configurations(
        id INTEGER AUTOINCREMENTING PRIMARY KEY,
        op INTEGER NOT NULL,
        FOREIGN KEY(op) REFERENCES operations(id)
    );
    
    # TODO: Finish adding fields
    CREATE TABLE IF NOT EXISTS listener_configurations(
        id INTEGER AUTOINCREMENTING,
        op INTEGER NOT NULL,
        FOREIGN KEY(op) REFERENCES operations(id)
    );
    
    # TODO: Finish adding fields
    CREATE TABLE IF NOT EXISTS agent_configurations(
        id INTEGER AUTOINCREMENTING PRIMARY KEY,
        op INTEGER NOT NULL,
        target_id INTEGER NOT NULL,
        FOREIGN KEY(op) REFERENCES operations(id),
        FOREIGN KEY(target_id) REFERENCES targets(id)
    );
    
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

# TODO: Implement support for schema changes
def create_db_tables_if_not_exists:
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(CREATE_SERPENT_DB_TABLES_COMMAND)
    conn.commit()
    conn.close()

def start_op(op_name):
    pass

def store_scan_results(results):
    pass

def query_table(table_name, params):
    pass

def query_targets(params):
    pass

def query_agents(params):
    pass

