
from mongoengine import Document, EmbeddedDocument
from mongoengine.fields import ReferenceField, DateTimeField, EmbeddedDocumentField, ListField, StringField, BooleanField


class Autor(Document):
    fullname = StringField(max_length=100)
    born_date = DateTimeField()
    born_location = StringField(max_length=100)
    description = StringField()

class Contact(Document):
    fullname = StringField(max_length=100, required=True)
    email = StringField(max_length=100, required=True)
    sent = BooleanField(default=False)
    phone_number = StringField(max_length=25)
    communication_method = StringField(max_length=10)
    meta = {'collection': 'contacts'}

class Tag(EmbeddedDocument):
    name = StringField()

class Post(Document):
    quote = StringField(required=True)
    author = ReferenceField(Autor)
    tags = ListField(EmbeddedDocumentField(Tag))
    meta = {'allow_inheritance': True}