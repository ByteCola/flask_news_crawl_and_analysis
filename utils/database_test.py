from database import Database

ExampleObj = Database()
db = ExampleObj.connect_database("tencent_news")
col = ExampleObj.get_collection("tencent_news", "tencent_new_collect")
ExampleObj.insert_data("tencent_news","tencent_new_collect", {'name': 'tencent', "id": 136})
ExampleObj.get_data("tencent_news","tencent_new_collect",)

#ExampleObj.drop_db(db)