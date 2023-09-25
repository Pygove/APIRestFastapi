from config.db import db_client

#db_client.counters.insert_one({"_id":"categoryID","sequence_value":0})
#db_client.counters.insert_one({"_id":"productsID","sequence_value":0})
def increment_couter(sequence_name):
    sequenceDocument = db_client.counters.find_one_and_update({"_id":sequence_name},{"$inc":{"sequence_value":1}})
    return sequenceDocument["sequence_value"]