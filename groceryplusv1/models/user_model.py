from mongoengine import Document, StringField, EmailField


class User(Document):
    """
    This Python class defines a User document with fields for ID, name, email, password, phone, image,
    and Stripe customer ID.
    """

    _id = StringField(primary_key=True)
    name = StringField(required=True)
    email = EmailField(required=True)
    password = StringField(required=True)
    phone = StringField(required=True)
    img = StringField()
    stripeCustomerId = StringField()

    def serialize(self):
        """
        The `serialize` function returns a dictionary containing specific attributes of an object.
        :return: The `serialize` method is returning a dictionary containing the following key-value
        pairs:
        - "_id": the value of `self._id`
        - "name": the value of `self.name`
        - "email": the value of `self.email`
        - "password": the value of `self.password`
        - "phone": the value of `self.phone`
        - "img": the value of `
        """
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
