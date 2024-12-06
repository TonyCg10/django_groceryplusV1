import json
from bson import ObjectId
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from groceryplusv1.models.product_model import Product


# pylint: disable=no-member
@csrf_exempt
def get_products(request):
    """
    The function `get_products` retrieves products based on filters from a request
    and returns a JSON
    response with the products or an error message.

    :param request: The `get_products` function takes a request object as a parameter.
    This request
    object likely contains information about the HTTP request being made,
    such as query parameters in
    the URL
    :return: The `get_products` function returns a JSON response with information about the
    products
    based on the filters provided in the request. If products are found based on the filters,
    it returns
    a success message along with the product data. If no products are found, it returns an
    error message
    indicating that products were not found. If an exception occurs during the process,
    it returns an
    error message with details about the exception
    """
    try:
        print("===== Request Log =====")
        print("Request Method:", request.method)
        print("Headers:", dict(request.headers))
        print("Body:", request.body.decode("utf-8"))
        print("========================")

        if request.method == "POST":
            data = json.loads(request.body)
            filters = {}

            for key, value in data.items():
                if isinstance(value, list):
                    filters[f"{key}__in"] = value
                else:
                    filters[key] = value

            products = (
                Product.objects.filter(**filters) if filters else Product.objects.all()
            )

            if not products:
                return JsonResponse(
                    {"success": False, "error": "Products not found"}, status=404
                )

            data = [product.serialize() for product in products]

            print("===== Response Log =====")
            print("Status: 200")
            print("Products Retrieved:", len(data))
            print("========================")

            return JsonResponse(
                {"success": True, "products": data, "message": "Products retrieved"},
                status=200,
            )

        return JsonResponse(
            {"success": False, "error": "Invalid request method"}, status=400
        )

    except Exception as e:
        print("===== Error Log =====")
        print("Error:", e)
        print("======================")

        return JsonResponse({"success": False, "error": str(e)}, status=500)


@csrf_exempt
def create_product(request):
    """
    The `create_product` function takes a POST request, extracts product data from the request body,
    creates a new product object, saves it to the database, and returns a JSON response with the new
    product details.

    :param request: The `create_product` function is designed to handle POST
    requests for creating a new
    product. It expects the request object to contain a JSON payload with the following parameters:
    :return: The `create_product` function returns a JSON response with information about the newly
    created product if the request method is POST and the product creation is
    successful. If the request
    method is not POST or an exception occurs during the process, it returns a
    JSON response indicating
    the failure along with an error message.
    """
    try:
        print("===== Request Log =====")
        print("Request Method:", request.method)
        print("Headers:", dict(request.headers))
        print("Body:", request.body.decode("utf-8"))
        print("========================")

        if request.method == "POST":

            data = json.loads(request.body)

            new_product_id = str(ObjectId())
            brand = data.get("brand")
            category = data.get("category")
            description = data.get("description")
            discount_percentage = data.get("discountPercentage")
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
                discountPercentage=discount_percentage,
                images=images,
                price=price,
                rating=rating,
                stock=stock,
                thumbnail=thumbnail,
                title=title,
            )
            new_product.save()

            print("===== User Created Log =====")
            print("User:", new_product.serialize())
            print("=============================")

            return JsonResponse(
                {
                    "success": True,
                    "product": new_product.serialize(),
                    "message": "Product created",
                },
                status=200,
            )
        return JsonResponse(
            {"success": False, "error": "Invalid request method"}, status=400
        )
    except Exception as e:
        print("===== Error Log =====")
        print("Error:", e)
        print("======================")

        return JsonResponse({"success": False, "error": str(e)}, status=500)


@csrf_exempt
def update_product(request, product_id):
    """
    The `update_product` function updates a product object in a database based on a PUT request with
    specified fields and returns a JSON response indicating success or failure.

    :param request: The `request` parameter in the `update_product` function is typically an HTTP
    request object that contains information about the incoming request, such as the request method
    (e.g., GET, POST, PUT, DELETE), headers, body, and other relevant data. In this context, the
    function is expecting
    :param id: The `id` parameter in the `update_product` function is used to identify the specific
    product that needs to be updated. It is typically the unique identifier of the product in the
    database, allowing the function to locate and modify the correct product information
    :return: The `update_product` function returns a JSON response with information about the success of
    updating a product. If the request method is PUT, it updates the product fields based on the data
    provided in the request body, saves the changes, and returns a success message along with the
    updated product data in JSON format. If the request method is not PUT, it returns an error message
    for an invalid request method.
    """
    try:
        print("===== Request Log =====")
        print(f"Request Method: {request.method}")
        print(f"Request Body: {request.body.decode('utf-8')}")
        print(f"Request Files: {request.FILES}")
        print("=======================")

        if request.method == "PUT":
            try:
                product = Product.objects.get(_id=product_id)
            except Product.DoesNotExist:
                return JsonResponse(
                    {"success": False, "error": "Product not found"}, status=404
                )

            update_fields = json.loads(request.body)

            for key, value in update_fields.items():
                if hasattr(product, key):
                    setattr(product, key, value)
                else:
                    print(f"Warning: Invalid field '{key}' provided. Skipping update.")

            product.save()

            product_data = product.serialize()

            print("===== Updated Product Log =====")
            print(f"Updated Product Data: {product_data}")
            print("===========================")

            return JsonResponse(
                {
                    "success": True,
                    "data": product_data,
                    "message": "Product updated",
                },
                status=200,
            )

        return JsonResponse(
            {"success": False, "error": "Invalid request method"}, status=400
        )

    except json.JSONDecodeError:
        return JsonResponse(
            {"success": False, "error": "Invalid JSON format"}, status=400
        )

    except Exception as e:
        print("===== Error Log =====")
        print("Error:", e)
        print("=====================")

        return JsonResponse({"success": False, "error": str(e)}, status=500)


@csrf_exempt
def delete_product(request, product_id):
    """
    This Python function deletes a product based on the provided ID in a RESTful API endpoint.

    :param request: The `request` parameter in the `delete_product` function is typically an HTTP
    request object that contains information about the incoming request, such as the request method
    (e.g., GET, POST, DELETE), headers, and data. In this context, the function is expecting a DELETE
    request to delete a
    :param id: The `id` parameter in the `delete_product` function is used to identify the specific
    product that needs to be deleted from the database. It is typically the unique identifier of the
    product in the database, such as a primary key or a specific field that uniquely identifies the
    product
    :return: The `delete_product` function returns a JSON response with a success status and message if
    the product is successfully deleted. If the request method is not DELETE, it returns a JSON response
    with a failure status and an error message indicating an invalid request method. If the product with
    the specified ID is not found, it returns a JSON response with a failure status and an error message
    indicating that the product was not
    """
    try:
        print("===== Request Log =====")
        print(f"Request Method: {request.method}")
        print(f"Request Body: {request.body.decode('utf-8')}")
        print(f"Request Files: {request.FILES}")
        print("=======================")

        if request.method == "DELETE":
            try:
                product = Product.objects.get(_id=product_id)
            except Product.DoesNotExist:
                return JsonResponse(
                    {"success": False, "error": "Product not found"}, status=404
                )

            product.delete()

            return JsonResponse(
                {"success": True, "message": "Product deleted"}, status=200
            )

        return JsonResponse(
            {"success": False, "error": "Invalid request method"}, status=400
        )

    except Exception as e:
        print("===== Error Log =====")
        print("Error:", e)
        print("=====================")
        return JsonResponse({"success": False, "error": str(e)}, status=500)


@csrf_exempt
def delete_all_product(request):
    """
    This function deletes all products from the database when a DELETE request is received.

    :param request: The `delete_all_product` function is designed to handle a DELETE request to delete
    all products from the database. If the request method is DELETE, it retrieves all products using
    `Product.objects.all()` and then deletes them. It returns a success message if the deletion is
    successful
    :return: The `delete_all_product` function returns a JSON response with a success message if the
    request method is DELETE and all products are successfully deleted. If the request method is not
    DELETE, it returns a JSON response with an error message indicating an invalid request method. If an
    exception occurs during the process, it returns a JSON response with the error message.
    """
    try:
        print("===== Request Log =====")
        print(f"Request Method: {request.method}")
        print(f"Request Body: {request.body.decode('utf-8')}")
        print(f"Request Files: {request.FILES}")
        print("=======================")

        if request.method == "DELETE":
            product = Product.objects.all()
            product.delete()

            return JsonResponse(
                {"success": True, "message": "Products deleted"}, status=200
            )

        return JsonResponse(
            {"success": False, "error": "Invalid request method"}, status=400
        )

    except Exception as e:
        print("===== Error Log =====")
        print("Error:", e)
        print("=====================")
        return JsonResponse({"success": False, "error": str(e)}, status=500)
