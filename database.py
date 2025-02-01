from pymongo import MongoClient
from config import MONGODB_URI, DATABASE_NAME
import bcrypt

client = MongoClient(MONGODB_URI)
db = client[DATABASE_NAME]

def create_user(username, password):
    if db.users.find_one({"username": username}):
        return False
    
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    user = {
        "username": username,
        "password": hashed
    }
    db.users.insert_one(user)
    return True

def verify_user(username, password):
    user = db.users.find_one({"username": username})
    if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
        return True
    return False

def save_shopping_list(username, list_name, items, people_count, days, total_cost):
    shopping_list = {
        "username": username,
        "list_name": list_name,
        "items": items,
        "people_count": people_count,
        "days": days,
        "total_cost": total_cost
    }
    db.shopping_lists.insert_one(shopping_list)

def get_user_lists(username):
    return list(db.shopping_lists.find({"username": username}))

def delete_list(username, list_name):
    db.shopping_lists.delete_one({"username": username, "list_name": list_name})
