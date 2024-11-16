import json
from bson import ObjectId
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from groceryplusv1.models.user_model import User


# pylint: disable=no-member
@csrf_exempt
def get_users(request):
    """
    The `get_users` function retrieves user data based on filters from a request and returns a JSON
    response with the results.

    :param request: The `get_users` function takes a `request` object as a parameter. This request
    object likely contains information about the HTTP request being made, such as query parameters in
    the URL (accessed through `request.GET.items()`). The function then processes these parameters to
    filter and retrieve user data from a
    :return: The `get_users` function returns a JSON response with information about the users based on
    the filters provided in the request. If users are found based on the filters, it returns a success
    message along with the user data. If no users are found, it returns a message indicating that users
    were not found. If an exception occurs during the process, it returns an error message with details
    about the exception.
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

            users = User.objects.filter(**filters) if filters else User.objects.all()

            if not users:
                return JsonResponse(
                    {"success": False, "error": "User not found"}, status=404
                )

            data = [user.serialize() for user in users]

            print("===== Response Log =====")
            print("Status: 200")
            print("Users Retrieved:", len(data))
            print("========================")

            return JsonResponse(
                {"success": True, "users": data, "message": "Users retrieved"},
                status=200,
            )

        return JsonResponse(
            {"success": False, "error": "Invalid request method"}, status=400
        )

    except Exception as e:
        print("===== Error Log =====")
        print("Error:", str(e))
        print("======================")

        return JsonResponse({"success": False, "error": str(e)}, status=500)


@csrf_exempt
def create_user(request):
    """
    The `create_user` function takes a POST request, extracts user data, creates a new user object,
    saves it to the database, and returns a JSON response with the new user details.

    :param request: The `create_user` function is designed to handle a POST request for creating a new
    user. It expects the request object to contain a JSON payload with the following parameters:
    :return: The `create_user` function returns a JSON response with the following structure:
    - If the request method is "POST" and the user creation is successful:
      - "success": True
      - "user": Serialized user data
      - "message": "User created"
      - Status code: 200
    - If the request method is not "POST":
      - "success": False
    """
    try:
        print("===== Request Log =====")
        print("Request Method:", request.method)
        print("Headers:", dict(request.headers))
        print("Body:", request.body.decode("utf-8"))
        print("========================")

        if request.method == "POST":
            data = json.loads(request.body)

            new_user_id = str(ObjectId())
            name = data.get("name")
            email = data.get("email")
            password = data.get("password")
            phone = data.get("phone")
            stripe_customer_id = data.get("stripeCustomerId")
            img = data.get("img")

            if not name or not email or not password or not phone:
                return JsonResponse(
                    {
                        "success": False,
                        "error": "Missing required fields: name, email, password, or phone",
                    },
                    status=400,
                )

            new_user = User(
                _id=new_user_id,
                name=name,
                email=email,
                password=password,
                phone=phone,
                img=img,
                stripeCustomerId=stripe_customer_id,
            )
            new_user.save()

            print("===== User Created Log =====")
            print("User:", new_user.serialize())
            print("=============================")

            return JsonResponse(
                {
                    "success": True,
                    "user": new_user.serialize(),
                    "message": "User created",
                },
                status=200,
            )
        else:
            return JsonResponse(
                {"success": False, "error": "Invalid request method"}, status=400
            )
    except Exception as e:
        print("===== Error Log =====")
        print("Error:", str(e))
        print("======================")

        return JsonResponse({"success": False, "error": str(e)}, status=500)


@csrf_exempt
def update_user(request, user_id):
    """
    The `update_user` function updates a user's information based on a PUT request, including handling
    image uploads.

    :param request: The `request` parameter in the `update_user` function is typically an HTTP request
    object that contains information about the incoming request, such as the request method (e.g., GET,
    POST, PUT, DELETE), request headers, request body, and any uploaded files. In this context, it seems
    :param id: The `id` parameter in the `update_user` function is used to identify the specific user
    that needs to be updated. It is typically the unique identifier of the user in the database, such as
    the primary key or a unique username
    :return: The `update_user` function returns a JSON response with information about the success of
    the user update operation. If the request method is PUT and the user is successfully updated, it
    returns a JSON response with a success message, updated user data, and a "User updated" message with
    a status code of 200. If the request method is not PUT, it returns a JSON response with an error
    message
    """
    try:
        print("===== Request Log =====")
        print(f"Request Method: {request.method}")
        print(f"Request Body: {request.body.decode('utf-8')}")
        print(f"Request Files: {request.FILES}")
        print("=======================")

        if request.method == "PUT":
            try:
                user = User.objects.get(_id=user_id)
            except User.DoesNotExist:
                return JsonResponse(
                    {"success": False, "error": "User not found"}, status=404
                )

            update_fields = json.loads(request.body)
            new_image = request.FILES.get("img")

            if new_image:
                update_fields["img"] = new_image

            for key, value in update_fields.items():
                if hasattr(user, key):
                    setattr(user, key, value)
                else:
                    print(f"Warning: Invalid field '{key}' provided. Skipping update.")

            user.save()

            user_data = user.serialize()

            print("===== Updated User Log =====")
            print(f"Updated User Data: {user_data}")
            print("===========================")

            return JsonResponse(
                {"success": True, "data": user_data, "message": "User updated"},
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
        print(f"Error: {str(e)}")
        print("=====================")
        return JsonResponse({"success": False, "error": str(e)}, status=500)


@csrf_exempt
def delete_user(request, user_id):
    """
    The `delete_user` function deletes a user based on the provided ID in a Django application and
    returns appropriate JSON responses for different scenarios.

    :param request: The `request` parameter in the `delete_user` function is typically an HTTP request
    object that contains information about the request made to the server, such as the request method
    (GET, POST, PUT, DELETE), headers, and data. In this context, the function is expecting an HTTP
    DELETE request
    :param id: The `id` parameter in the `delete_user` function is used to specify the unique identifier
    of the user that needs to be deleted from the database. This identifier is typically used to locate
    the specific user record that should be removed
    :return: The `delete_user` function returns a JSON response with a success message if the user is
    successfully deleted, or an error message if there are any issues such as the user not being found
    or encountering an exception. The specific response returned depends on the outcome of the deletion
    operation and any potential errors that may occur.
    """
    try:
        print("===== Request Log =====")
        print(f"Request Method: {request.method}")
        print(f"Request Body: {request.body.decode('utf-8')}")
        print(f"Request Files: {request.FILES}")
        print("=======================")

        if request.method == "DELETE":
            try:
                user = User.objects.get(_id=user_id)
            except User.DoesNotExist:
                return JsonResponse(
                    {"success": False, "error": "User not found"}, status=404
                )

            user.delete()

            return JsonResponse(
                {"success": True, "message": "User deleted"}, status=200
            )

        return JsonResponse(
            {"success": False, "error": "Invalid request method"}, status=400
        )

    except Exception as e:
        print("===== Error Log =====")
        print(f"Error: {str(e)}")
        print("=====================")
        return JsonResponse({"success": False, "error": str(e)}, status=500)
