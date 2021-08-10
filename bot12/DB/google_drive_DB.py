from DB.conf import BASE,SESSION
import pickle
import threading
from sqlalchemy import Column, Integer, String, LargeBinary


class gDriveCreds(BASE):
    __tablename__ = "gDrive"
    chat_id = Column(Integer, primary_key=True)
    credential_string = Column(LargeBinary)
    name = Column(String)


    def __init__(self, chat_id):
        self.chat_id = chat_id

# gDriveCreds.__table__.drop()

gDriveCreds.__table__.create(checkfirst=True)


INSERTION_LOCK = threading.RLock()

def _set(chat_id, credential_string,name):
    with INSERTION_LOCK:
        saved_cred = SESSION.query(gDriveCreds).get(chat_id)
        if not saved_cred:
            saved_cred = gDriveCreds(chat_id)

            saved_cred.credential_string = pickle.dumps(credential_string) 
            saved_cred.name = name     
        else:
            print('already exist')
        SESSION.add(saved_cred)
        SESSION.commit()

def _chek(chat_id):

    with INSERTION_LOCK:
        saved_cred = SESSION.query(gDriveCreds).get(chat_id)

        if saved_cred:
            return True
        return False


def search(chat_id):
    with INSERTION_LOCK:
        saved_cred = SESSION.query(gDriveCreds).get(chat_id)
        creds = None
        if saved_cred is not None:
            creds = pickle.loads(saved_cred.credential_string)
        return creds



def _clear(chat_id):
    with INSERTION_LOCK:
        saved_cred = SESSION.query(gDriveCreds).get(chat_id)
        if saved_cred:
            SESSION.delete(saved_cred)
            SESSION.commit()

def _get_add():
    with INSERTION_LOCK:
        saved_cred = SESSION.query(gDriveCreds).all()
        if saved_cred:
            return saved_cred
            # for i in saved_cred:
            #     print(i)
            # print(i.chat_id,i.name,i.credential_string,'\n')



# _set(1123344)
# _clear(1)

print(_get_add())