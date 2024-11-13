from mongoengine import Document, StringField, EmailField


class User(Document):
    _id = StringField()
    name = StringField()
    email = EmailField()
    password = StringField()
    phone = StringField()
    img = StringField()
    stripeCustomerId = StringField()

    def serialize(self):
        return {
            "_id": self._id,
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "phone": self.phone,
            "img": self.img if self.img else None,
            "stripeCustomerId": self.stripeCustomerId,
        }

    meta = {"collection": "users"}
