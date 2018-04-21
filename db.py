import sqlite3

# TODO: Implement and integrate
class SerpentDb:
    DB_NAME = 'serpent'

    TABLES = {
        'operations' => {
            'columns' => {
                'id' => {
                    'type' => 'integer autoincrementing'
                },
                'op_name' => {
                    'type' => 'text'
                },
                'is_current' => {
                    'type' => 'boolean'
                },
                'creation_date' => {
                    'type' => 'date'
                }
            },
            'primary_key' => 'id'
        },
        'agents' => {
            'columns' => {
                'id' => {
                    'type' => 'integer autoincrementing'
                },
                'op' => {
                    'type' => 'integer'
                },
                'configuration' => {
                    'type' => 'integer'
                }
            },
            'primary_key' => 'id',
            'foreign_keys' => {
                'op' => 'operations.id',
                'configuration' => 'agent_configurations.id'
            }
        },
        'listeners' => {
            'columns' => {
                'id' => {
                    'type' => 'integer autoincrementing'
                },
                'op' => {
                    'type' => 'integer'
                },
                'configuration' => {
                    'type' => 'integer'
                }
            },
            'primary_key' => 'id',
            'foreign_keys' => {
                'op' => 'operations.id',
                'configuration' => 'listener_configurations.id'
            }
        },
        'targets' => {
            'columns' => {
                'id' => {
                    'type' => 'integer autoincrementing'
                },
                'ip' => {
                    'type' => 'text'
                },
                'hostname' => {
                    'type' => 'text'
                },
                'os' => {
                    'type' => 'text'
                }
            },
            'primary_key' => 'id'
        },
        'payload_configurations' => {
            'columns' => {
                'id' => {
                    'type' => 'integer autoincrementing'
                },
                'op' => {
                    'type' => 'integer'
                },
                # TODO: Finish defining
                # '' => {
                #     'type' => ''
                # },
                # '' => {
                #     'type' => ''
                # },
                # '' => {
                #     'type' => ''
                # },
                # '' => {
                #     'type' => ''
                # },
                # '' => {
                #     'type' => ''
                # }
            },
            'primary_key' => 'id',
            'foreign_keys' => {
                'op' => 'operations.id'
            }
        },
        'listener_configurations' => {
            'columns' => {
                'id' => {
                    'type' => 'integer autoincrementing'
                },
                'op' => {
                    'type' => 'integer'
                },
                # TODO: Finish defining
                # '' => {
                #     'type' => ''
                # },
                # '' => {
                #     'type' => ''
                # },
                # '' => {
                #     'type' => ''
                # },
                # '' => {
                #     'type' => ''
                # },
                # '' => {
                #     'type' => ''
                # }
            },
            'primary_key' => 'id',
            'foreign_keys' => {
                'op' => 'operations.id'
            }
        },
        'agent_configurations' => {
            'columns' => {
                'id' => {
                    'type' => 'integer autoincrementing'
                },
                'op' => {
                    'type' => 'integer'
                },
                # TODO: Finish defining
                # '' => {
                #     'type' => ''
                # },
                # '' => {
                #     'type' => ''
                # },
                # '' => {
                #     'type' => ''
                # },
                # '' => {
                #     'type' => ''
                # },
                # '' => {
                #     'type' => ''
                # }
            },
            'primary_key' => 'id',
            'foreign_keys' => {
                'op' => 'operations.id'
            }
        },
        'port_scan_results' => {
            'columns' => {
                'id' => {
                    'type' => 'integer autoincrementing'
                },
                'op' => {
                    'type' => 'integer'
                },
                'target_id' => {
                    'type' => 'id'
                },
                'port' => {
                    'type' => 'integer'
                },
                'status' => {
                    'type' => 'text'
                },
                'scan_time' => {
                    'type' => 'date'
                }
            },
            'primary_key' => 'id',
            'foreign_keys' => {
                'op' => 'operations.id',
                'target_id' => 'targets.id'
            }
        },
        # TODO: Add any other necessary tables
        # '' => {
        #     'columns' => {
        #         '' => {
        #             'type' => ''
        #         },
        #         '' => {
        #             'type' => ''
        #         },
        #         '' => {
        #             'type' => ''
        #         },
        #         '' => {
        #             'type' => ''
        #         },
        #         '' => {
        #             'type' => ''
        #         }
        #     },
        #     'primary_key' => ''
        # }
    }

    def __init__(self):
        pass

    def create_tables(self):
        # TODO: Parse the table definitions and create the tables (if they don't exist)
        pass
