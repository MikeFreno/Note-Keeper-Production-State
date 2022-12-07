from rest_framework import viewsets, generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view
import os
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from dotenv import load_dotenv, find_dotenv
from .serializers import UserSerializer
from .models import User
from .permissions import IsLoggedInUserOrAdmin, IsAdminUser


class UserView(viewsets.ModelViewSet, generics.UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def patch(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def get_permissions(self):
        permission_classes = []
        if self.action == "create":
            permission_classes = [AllowAny]
        elif (
            self.action == "retrieve"
            or self.action == "update"
            or self.action == "partial_update"
        ):
            permission_classes = [IsLoggedInUserOrAdmin]
        elif self.action == "list" or self.action == "destroy":
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


@api_view(["GET"])
def user_state(request):
    if request.user.is_anonymous:
        return Response("false")
    else:
        response = Response()
        response.data = request.user.email, request.user.id
        return response


@api_view(["POST"])
def registration_emailer(request):
    configuration = sib_api_v3_sdk.Configuration()
    load_dotenv(find_dotenv())
    KEY = os.environ["SENDINBLUE_KEY"]
    configuration.api_key["api-key"] = KEY
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
        sib_api_v3_sdk.ApiClient(configuration)
    )
    subject = "Thank you!"
    sender = {"name": "Michael Freno", "email": "mike@notesapp.net"}
    templateId = 2
    to = [{"email": request.user.email}]
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=to,
        template_id=templateId,
        sender=sender,
        subject=subject,
    )
    try:
        api_response = api_instance.send_transac_email(send_smtp_email)
        print(api_response)
        return Response("Success")
    except ApiException as e:
        print("Exception when calling S`MTPApi->send_transac_email: %s\n" % e)
        return Response(
            "Exception when calling S`MTPApi->send_transac_email: view console log"
        )
