from mongoengine import Document, StringField, IntField, ListField


class Product(Document):
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
