from peewee import (
    Model,

    MySQLDatabase,

    CharField,
    IntegerField,
    TextField,
    DateTimeField,
    FloatField,
    BooleanField,
)


db = quick_alert_db = MySQLDatabase(
    'quickalert',
    user='quickalert', password='quickalert',
    host='127.0.0.1', port=3306
)


class Annonce(Model):
    id = CharField(unique=True, primary_key=True)
    site = CharField()
    created = DateTimeField()
    title = CharField()
    description = TextField(null=True)
    telephone = TextField(null=True)
    price = FloatField()
    charges = FloatField(null=True)
    surface = FloatField()
    rooms = IntegerField()
    bedrooms = IntegerField(null=True)
    city = CharField()
    link = CharField()
    picture = CharField(null=True)
    posted2trello = BooleanField(default=False)

    class Meta:
        database = db
        order_by = ('-created',)


#def create_tables():
#    with db:
#        db.create_tables([Annonce])
