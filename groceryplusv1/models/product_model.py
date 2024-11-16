from mongoengine import Document, StringField, IntField, ListField


class Product(Document):
    """
    This Python class defines a Product document with various fields and a serialize method for data
    serialization.
    """

    _id = StringField(primary_key=True)
    brand = StringField()
    category = StringField()
    description = StringField()
    discountPercentage = IntField()
    images = ListField(StringField())
    price = IntField()
    rating = IntField()
    stock = IntField()
    thumbnail = StringField()
    title = StringField()

    def serialize(self):
        """
        The `serialize` function returns a dictionary containing various attributes of an object.
        :return: The `serialize` method is returning a dictionary containing the attributes of an
        object. The keys in the dictionary are "_id", "brand", "category", "description",
        "discountPercentage", "images", "price", "rating", "stock", "thumbnail", and "title", with their
        corresponding values being the values of those attributes in the object.
        """
        return {
            "_id": self._id,
            "brand": self.brand,
            "category": self.category,
            "description": self.description,
            "discountPercentage": self.discountPercentage,
            "images": self.images,
            "price": self.price,
            "rating": self.rating,
            "stock": self.stock,
            "thumbnail": self.thumbnail,
            "title": self.title,
        }

    meta = {"collection": "products"}
