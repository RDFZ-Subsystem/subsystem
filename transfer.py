import pymongo
import dbConnecter


client = pymongo.MongoClient()
db = client.reciter

'''
集合名articles

    id 文章id
    username 用户名
    title 标题
    content 内容
    timef 发布时间
    top 是否置顶

    
    CREATE TABLE articles (
        id VARCHAR(128), 
        username VARCHAR(64), 
        title VARCHAR(128), 
        content TEXT, 
        timef VARCHAR(64), 
        top BOOL
    );

'''

def toStr(l):
    str = ''
    for i in l:
        str += i
        str += '|'
    return str


list1 = list(db.lists.find())
list2 = list(db.articles.find())
for i in list2:
    dbConnecter.insert_data('articles',
                            '(id, username, title, content, timef, top)',
                            (i['id'], i['username'], i['title'], i['content'], i['timef'], i['top'])
                            )