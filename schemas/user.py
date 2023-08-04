def user_schema(user) -> dict:
    return{'id':str(user['_id']),
           'Nombre':user["first_name"],
           'Apellido':user['last_name'],
           'Email':user['email'],
           'Usuario':user['username']}

def users_schema(users) -> list:
    return [user_schema(user) for user in users]