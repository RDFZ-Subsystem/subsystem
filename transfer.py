import pymongo
import dbConnecter


client = pymongo.MongoClient()
db = client.reciter

''''
    集合名users

    username 用户名
    password 密码
    timef 注册时间
    intro 个人简介
    theme 颜色主题
    admin 是否为管理员

    CREATE TABLE users (
        username VARCHAR(64), 
        password VARCHAR(64), 
        timef VARCHAR(64), 
        intro TEXT, 
        theme VARCHAR(64), 
        admin BOOL
    );
'''

list1 = list(db.users.find())
for i in list1:
    dbConnecter.insert_data('users',
                            '(username, password, timef, intro, theme, admin)',
                            (i['username'], i['password'], i['timef'], i['intro'], i['theme'], i['admin'])
                            )