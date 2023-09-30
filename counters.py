from config.db import db_client

db_client.counters.insert_one({"_id":"categoryID","sequence_value":0})
db_client.counters.insert_one({"_id":"productsID","sequence_value":0})
db_client.counters.insert_one({"_id":"usersID","sequence_value":0})