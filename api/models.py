from mongoengine import Document, IntField, StringField

class Name_Stats(Document):
    year = IntField(required=True)
    firstname = StringField(required=True)
    gender = StringField(required=True, max_length=1)
    nb_occur = IntField(required=True)
    
    meta = {
        "indexes": [
            "+year",
            "$firstname"
        ]
    }