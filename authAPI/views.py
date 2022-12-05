from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, To, From, Subject
from dotenv import load_dotenv, find_dotenv
from .serializers import UserSerializer
from .models import User
from .permissions import IsLoggedInUserOrAdmin, IsAdminUser


class UserView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

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
    load_dotenv(find_dotenv())
    SECRET_KEY = os.environ["SENDGRID_API_KEY"]
    message = Mail()
    message.to = [
        To(
            email=request.user.email,
        ),
    ]
    message.from_email = From(
        email="michael@freno.me",
        name="Michael Freno",
    )
    message.subject = Subject("Thanks for Registering!")
    message.template_id = "d-5a4e7a8e000c4ea3b89cb4763f243653"
    sendgrid_client = SendGridAPIClient(SECRET_KEY)

    response = sendgrid_client.send(message)
    return Response(response.status_code)
