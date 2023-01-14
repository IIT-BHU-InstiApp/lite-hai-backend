from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from .models import LostAndFound
from .serializers import (
    CreateLostAndFoundSerializer,
    LostAndFoundSerializer,
    LostAndFoundListSerializer)
from googleapiclient.discovery import build
from google.oauth2 import service_account

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'keys.json'

cred = None
cred = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

LOST_AND_FOUND_SPREADSHEET_ID = '1Hch-gohmuAeAeJFwaozb1xz_Oj7DLa6C0qOhAuk3t-o'


class CreateLostAndFoundView(GenericAPIView):
    """
    post:
    Creates a new lost and found object and returns the
    Id, Name, Branch, Course, Year, Type and Description of the object.
    """
    permission_classes = (permissions.IsAuthenticated,)
    # pylint: disable=no-member
    queryset = LostAndFound.objects.all()
    serializer_class = CreateLostAndFoundSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        complaint = serializer.save()
        complaint_dict = LostAndFoundSerializer(complaint)
        service = build('sheets', 'v4', credentials=cred)
        sheet = service.spreadsheets()
        sheet.values().append(
            spreadsheetId=LOST_AND_FOUND_SPREADSHEET_ID,
            range="lost_and_found!A1:H1",
            valueInputOption="USER_ENTERED",
            insertDataOption="INSERT_ROWS",
            body={
                "values": [[
                    complaint_dict.data['id'],
                    complaint_dict.data['name'],
                    complaint_dict.data['branch'],
                    complaint_dict.data['course'],
                    complaint_dict.data['year'],
                    complaint_dict.data['type_of_lost_and_found'],
                    complaint_dict.data['description'],
                    complaint_dict.data['drive_link']
                ]]
            }
        ).execute()
        return Response(complaint_dict.data, status=status.HTTP_201_CREATED)


class LostAndFoundListView(GenericAPIView):
    """
    get:
    Returns the list of all lost and found objects created by the authenticated user
    """
    permission_classes = (permissions.IsAuthenticated,)
    # pylint: disable=no-member
    queryset = LostAndFound.objects.all()
    serializer_class = LostAndFoundListSerializer

    def get(self, request):
        serializer = self.get_serializer()
        list_lost_and_found = serializer.get_list()
        list_lost_and_found_dict = LostAndFoundSerializer(
            list_lost_and_found, many=True)
        return Response(list_lost_and_found_dict.data, status=status.HTTP_200_OK)
