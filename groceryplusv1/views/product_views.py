from bson import ObjectId
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from groceryplusv1.models.product_model import Product


@csrf_exempt
def get_products(request):
    try:
        filters = {}

        for key, value in request.GET.items():
            filters[key] = value

        if filters:
            products = Product.objects.filter(**filters)
        else:
            products = Product.objects.all()

        data = [product.serialize() for product in products]

        if products:
            return JsonResponse(
                {"success": True, "products": data, "message": "Products gotten"},
                status=200,
            )
        else:
            return JsonResponse(
                {"success": False, "error": "Products not found"}, status=404
            )
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)


@csrf_exempt
def create_product(request):
    try:
        if request.method == "POST":
            data = json.loads(request.body)
            new_product_id = str(ObjectId())
            brand = data.get("brand")
            category = data.get("category")
            description = data.get("description")
            discountPercentage = data.get("discountPercentage")
            images = data.get("images")
            price = data.get("price")
            rating = data.get("rating")
            stock = data.get("stock")
            thumbnail = data.get("thumbnail")
            title = data.get("title")

            new_product = Product(
                _id=new_product_id,
                brand=brand,
                category=category,
                description=description,
                discountPercentage=discountPercentage,
                images=images,
                price=price,
                rating=rating,
                stock=stock,
                thumbnail=thumbnail,
                title=title,
            )

            new_product.save()

            print("#####" + str(new_product))

            return JsonResponse(
                {
                    "success": True,
                    "product": new_product.serialize(),
                    "message": "Product created",
                },
                status=200,
            )
        else:
            return JsonResponse(
                {"success": False, "error": "Invalid request method"}, status=400
            )
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)


@csrf_exempt
def update_product(request, id):
    try:
        if request.method == "PUT":
            product = Product.objects.get(_id=id)
            update_fields = json.loads(request.body)

            for key, value in update_fields.items():
                setattr(product, key, value)

            product.save()

            print("#####" + str(product))

            return JsonResponse(
                {
                    "success": True,
                    "data": product.to_json(),
                    "message": "Product updated",
                },
                status=200,
            )
        else:
            return JsonResponse(
                {"success": False, "error": "Invalid request method"}, status=400
            )

    except Product.DoesNotExist:
        return JsonResponse(
            {"success": False, "error": "Product not found"}, status=404
        )
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)


@csrf_exempt
def delete_product(request, id):
    try:
        if request.method == "DELETE":
            product = Product.objects.get(_id=id)
            product.delete()

            return JsonResponse(
                {"success": True, "message": "Product deleted"}, status=200
            )

        else:
            return JsonResponse(
                {"success": False, "error": "Invalid request method"}, status=400
            )

    except Product.DoesNotExist:
        return JsonResponse(
            {"success": False, "error": "Product not found"}, status=404
        )
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)


@csrf_exempt
def delete_all_product(request):
    try:
        if request.method == "DELETE":
            product = Product.objects.all()
            product.delete()

            return JsonResponse(
                {"success": True, "message": "Products deleted"}, status=200
            )

        else:
            return JsonResponse(
                {"success": False, "error": "Invalid request method"}, status=400
            )
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)
