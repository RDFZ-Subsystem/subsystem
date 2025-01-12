import pymongo
import uuid


client = pymongo.MongoClient()
db = client.reciter

'''
    集合名 yule

    name 游戏名
    hot 游戏热度
    path 游戏html文件路径
    intro 游戏介绍路径
    timef 创建时间
    creator 创建者
'''


db.yule.add_one({
     'name': 'FruitNinja',
     'hot': 0,
     'path': 'yule/source/FruitNinjaGame.html',
     'intro': 'templates/yule/intro/FruitNinjaGameIntro.md',
     'timef': '2025-01-03 09:06',
     'creator': 'ycy'
})
