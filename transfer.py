import pymongo
import dbConnecter


client = pymongo.MongoClient()
db = client.reciter

'''

    
'''

def toStr(l):
    str = ''
    for i in l:
        str += i
        str += '|'
    return str


list1 = list(db.lists.find())
list2 = list(db.articles.find())
for i in list1:
    dbConnecter.insert_data('lists',
                            '(id, username, listname, difficulty, en, zh, timef, o, sm, sen)',
                            (i['id'], i['username'], i['listname'], i['difficulty'], toStr(i['en']), toStr(i['zh']), i['timef'], i['o'], i['sm'], toStr(i['sen']))
                            )