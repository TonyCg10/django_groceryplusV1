from bson import ObjectId
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from groceryplusv1.models.user_model import User


@csrf_exempt
def get_users(request):
    try:
        filters = {}

        for key, value in request.GET.items():
            filters[key] = value

        if filters:
            users = User.objects.filter(**filters)
        else:
            users = User.objects.all()

        data = [user.serialize() for user in users]

        print(data)

        if data == []:
            return JsonResponse(
                {
                    "success": False,
                    "users": [],
                    "message": "Users not found",
                },
                status=404,
            )

        return JsonResponse(
            {"success": True, "users": data, "message": "Users retrieved"},
            status=200,
        )

    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)


@csrf_exempt
def create_user(request):
    try:
        if request.method == "POST":
            data = json.loads(request.body)
            new_user_id = str(ObjectId())
            name = data.get("name")
            email = data.get("email")
            password = data.get("password")
            phone = data.get("phone")
            stripeCustomerId = data.get("stripeCustomerId")
            img = data.get("img")

            new_user = User(
                _id=new_user_id,
                name=name,
                email=email,
                password=password,
                phone=phone,
                img=img,
                stripeCustomerId=stripeCustomerId,
            )
            new_user.save()

            print("#####" + str(new_user))

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
        return JsonResponse({"success": False, "error": str(e)}, status=500)


@csrf_exempt
def update_user(request, id):
    try:
        if request.method == "PUT":
            user = User.objects.get(_id=id)
            update_fields = json.loads(request.body)
            new_image = request.FILES.get("img")

            if new_image:
                update_fields["img"] = new_image

            for key, value in update_fields.items():
                setattr(user, key, value)

            user.save()

            user_data = user.serialize()

            return JsonResponse(
                {"success": True, "data": user_data, "message": "User updated"},
                status=200,
            )

        else:
            return JsonResponse(
                {"success": False, "error": "Invalid request method"}, status=400
            )

    except User.DoesNotExist:
        return JsonResponse({"success": False, "error": "User not found"}, status=404)
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)


@csrf_exempt
def delete_user(request, id):
    try:
        if request.method == "DELETE":
            user = User.objects.get(_id=id)
            user.delete()

            return JsonResponse(
                {"success": True, "message": "User deleted"}, status=200
            )

        else:
            return JsonResponse(
                {"success": False, "error": "Invalid request method"}, status=400
            )

    except User.DoesNotExist:
        return JsonResponse({"success": False, "error": "User not found"}, status=404)
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)
