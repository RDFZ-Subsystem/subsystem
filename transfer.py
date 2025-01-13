import pymongo
import pymysql
import json
from pymongo.errors import ConnectionError

# MongoDB 配置
MONGO_URI = "mongodb://localhost:27017"
MONGO_DB = "your_mongodb_database"

# MySQL 配置
MYSQL_HOST = "localhost"
MYSQL_USER = "root"
MYSQL_PASSWORD = "your_mysql_password"
MYSQL_DB = "your_mysql_database"


# 连接 MongoDB
def connect_to_mongo():
    try:
        client = pymongo.MongoClient(MONGO_URI)
        db = client[MONGO_DB]
        return db
    except ConnectionError as e:
        print(f"连接 MongoDB 失败: {e}")
        return None


# 连接 MySQL
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


# 创建 MySQL 表 (根据 MongoDB 集合的字段)
def create_mysql_table(cursor, collection_name, sample_data):
    fields = sample_data.keys()
    columns = []
    for field in fields:
        column_type = "TEXT"  # 默认使用 TEXT 类型
        columns.append(f"`{field}` {column_type}")
    columns_str = ", ".join(columns)

    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS `{collection_name}` (
        `id` INT AUTO_INCREMENT PRIMARY KEY,
        {columns_str}
    )
    """
    cursor.execute(create_table_query)


# 将 MongoDB 数据插入 MySQL
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


# 从 MongoDB 获取集合数据
def fetch_mongo_data(db):
    collections = db.list_collection_names()
    mongo_data = {}

    for collection_name in collections:
        collection = db[collection_name]
        data = list(collection.find())
        mongo_data[collection_name] = data

    return mongo_data


# 主函数
def migrate_data():
    # 连接到 MongoDB
    mongo_db = connect_to_mongo()
    if not mongo_db:
        return

    # 连接到 MySQL
    mysql_connection = connect_to_mysql()
    if not mysql_connection:
        return

    # 获取 MongoDB 数据
    mongo_data = fetch_mongo_data(mongo_db)

    # 获取 MySQL 游标
    cursor = mysql_connection.cursor()

    # 遍历每个 MongoDB 集合，迁移数据到 MySQL
    for collection_name, data in mongo_data.items():
        # 创建 MySQL 表
        create_mysql_table(cursor, collection_name, data)

        # 插入数据到 MySQL
        insert_data_to_mysql(cursor, collection_name, data)
        mysql_connection.commit()
        print(f"成功迁移集合 `{collection_name}` 数据到 MySQL")

    # 关闭 MySQL 连接
    cursor.close()
    mysql_connection.close()
    print("数据迁移完成！")


if __name__ == "__main__":
    migrate_data()
