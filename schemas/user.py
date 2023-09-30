def user_schema(user) -> dict:
    return{
           'id':user["_id"],
           'username':user["username"],
           'first_name':user['first_name'],
           'last_name':user['last_name'],
           'email':user['email'],
           'password':user['password'],
           'gender':str(user['gender']),
           'role' : user['role'],
           'avatar' : user['avatar'],
            "creation_date":user["creation_date"],
            "last_modification_date":user["last_modification_date"]
    }

def users_schema(users) -> list:
    return [user_schema(user) for user in users]