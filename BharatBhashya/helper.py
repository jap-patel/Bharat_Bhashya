from pymongo import MongoClient
import ssl
import urllib

def connect_to_db(collection_name):
    USER_NAME = r"abimanyu"
    PASSWORD = r"26417"
    client = MongoClient(f"mongodb+srv://{USER_NAME}:{PASSWORD}@analytics.gf6av.mongodb.net/test",ssl_cert_reqs=ssl.CERT_NONE)

    # PASSWORD=urllib.parse.quote_plus("abd@")
    # client = pymongo.MongoClient(f"mongodb+srv://{USER_NAME}:{PASSWORD}@cluster0.xqmbf.mongodb.net/myFirstDatabase?retryWrites=true&w=majority",ssl_cert_reqs=ssl.CERT_NONE)

    db = client.Bharat_Bhashya    
    if collection_name == 'users':
        coll = db.users
        return [db, client, coll]
    elif collection_name == 'cases':
        coll = db.cases
        return [db, client, coll]
    elif collection_name == 'sessions':
        coll = db.sessions
        return [db, client, coll]
    elif collection_name == 'security_agencies':
        coll = db.security_agencies
        return [db, client, coll]
    elif collection_name == 'admin_user':
        coll = db.admin_user
        return [db, client, coll]
    else:
        return "nothing_to_return"

def password_check(passwd):
      
    SpecialSym =['$', '@', '#', '%', '!', '*', '?', '&']
      
    if len(passwd) < 6:
        return "length should be at least 6"        
          
    if len(passwd) > 20:
        return "length should be not be greater than 20"        
          
    if not any(char.isdigit() for char in passwd):
        return "Password should have at least one numeral"        
          
    if not any(char.isupper() for char in passwd):
        return "Password should have at least one uppercase letter"
        
    if not any(char.islower() for char in passwd):
        return "Password should have at least one lowercase letter"       
          
    if not any(char in SpecialSym for char in passwd):
        return "Password should have at least one SpecialSymbol"      

def get_speech_language(language):
    if language == "Gujarati":
        return "gu-IN"
    elif language == "English":  
        return "en-IN"
    elif language == "Hindi":
        return "hi-IN"
    elif language == "Bengali": 
        return "bn-IN"
    elif language == "Kanada":
        return "kn-IN"
    elif language == "Telegu": 
        return "te-IN"
    elif language == "Urdu":
        return "ur-IN"
    elif language == "Malayalam":
        return "ml-IN"
    elif language == "Tamil":
        return "ta-IN"

def get_text_language(language):
    if language == "Gujarati":
        return "gu"
    elif language == "English":  
        return "en"
    elif language == "Hindi":
        return "hi"
    elif language == "Bengali": 
        return "bn"
    elif language == "Kanada":
        return "kn"
    elif language == "Telegu": 
        return "te"
    elif language == "Urdu":
        return "ur"
    elif language == "Malayalam":
        return "ml"
    elif language == "Tamil":
        return "ta"