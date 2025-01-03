from sqlalchemy import create_engine
from sqlalchemy import text

def parse(list_str):
    list_str = list_str.split("['")[1:][0]
    list_str = list_str.split("']")[:-1][0]
    real_list = list_str.split("', '")

    return real_list

# CONNECTION
def db(db_config):
    if db_config['dialect'] == 'sqlite':
        url = f"{db_config['dialect']}:///{db_config['database']}.db" # SQLite
    else:
        url = f"{db_config['dialect']}+{db_config['driver']}://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}" # MySQL

    engine = create_engine(url)
    conn = engine.connect()

    # CURSOR
    # no cursor

    # COMMAND
    simplified_file = {}
    stmt = text("SELECT id, ingredient FROM NinJiom")

    results = conn.execute(stmt)

    for row in results:
        if row[0] <= 8 or row[0] >= 15:
            simplified_file[row[0]] = parse(row[1])
        elif row[0] == 9:
            simplified_file[row[0]] = ['採用純天然植物，獨特口味，清涼潤喉。']

    return str(simplified_file)

def db2(db_config, result):
    if db_config['dialect'] == 'sqlite':
        url = f"{db_config['dialect']}:///{db_config['database']}.db" # SQLite
    else:
        url = f"{db_config['dialect']}+{db_config['driver']}://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}" # MySQL

    engine = create_engine(url)
    conn = engine.connect()

    # CURSOR
    # no cursor

    # COMMAND
    if len(result) != 1:
        stmt = text(f"SELECT * FROM NinJiom WHERE id IN {str(tuple(result))}")
    else:
        stmt = text(f"SELECT * FROM NinJiom WHERE id = {str(result[0])}")

    results = conn.execute(stmt)

    response = []

    for row in results:
        # (12, 'https://cdn.sanity.io/images/dddbuyhi/production/6aed2c87f3854af7993d0374aaa2dd9718db1d98-9130x3800.jpg', 'herbal-candy-series', '京都念慈菴 枇杷潤喉糖 - 烏梅味', '採用純天然植物，配以烏梅精心煉製，生津解渴，清涼潤喉。', "['採用純天然植物，配以烏梅精心煉製，生津解渴，清涼潤喉。']")
        if row[0] < 9 or row[0] > 14:
            item = {
                "img": row[1],
                "category": row[2],
                "product": row[3],
                "description": row[4],
                "ingredient": row[5] # (ingredient: purpose)
            }
        else:
            item = {
                "img": row[1],
                "category": row[2],
                "product": row[3],
                "description": row[4],
                "ingredient": ["糖", "葡萄糖漿","水", "植物抽出物", "香料"]
            }
        response.append(item)

    return response

def prompt_creator(INITIAL_PROMPT, db_config):
    simplified_file_str = db(db_config)
    INITIAL_PROMPT += simplified_file_str
    return INITIAL_PROMPT