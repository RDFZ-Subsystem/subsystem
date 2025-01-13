import pymysql


MYSQL_HOST = "localhost"
MYSQL_USER = "root"
MYSQL_PASSWORD = "your_mysql_password"
MYSQL_DB = "your_mysql_database"


def connect_to_mysql():
    try:
        connection = pymysql.connect(host=MYSQL_HOST,
                                     user=MYSQL_USER,
                                     password=MYSQL_PASSWORD,
                                     database=MYSQL_DB)
        return connection
    except pymysql.MySQLError as e:
        print(f"连接 MySQL 失败: {e}")
        return None

def insert_data_to_mysql(cursor, collection_name, data):
    if not data:
        return

    # 构建插入数据的 SQL 语句
    columns = data[0].keys()
    columns_str = ", ".join([f"`{col}`" for col in columns])
    values_placeholder = ", ".join(["%s"] * len(columns))

    insert_query = f"INSERT INTO `{collection_name}` ({columns_str}) VALUES ({values_placeholder})"

    # 插入数据
    for item in data:
        values = tuple(item.get(col, None) for col in columns)
        cursor.execute(insert_query, values)

