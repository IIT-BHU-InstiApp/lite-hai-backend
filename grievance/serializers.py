from rest_framework import serializers
from .models import Complaint


class CreateGrievanceSerializer(serializers.Serializer):
    TYPE = (('Security', "Security"), ('Health&Hygiene', "Health&Hygiene"), ('HostelMess',
                                                                             "HostelMess"), ('Academics', "Academics"), ('Council', "Council"), ('Others', "Others"))
    YEAR = (('1st', "1st"), ('2nd', "2nd"),
            ('3rd', "3rd"), ('4th', "4th"), ('5th', "5th"))
    COURSE = (('B.Tech', "B.Tech"), ('IDD', "IDD"), ('M.Tech', "M.Tech"))
    BRANCH = (('Architecture', "Architecture"), ('Ceramic', "Ceramic"), ('Chemical', "Chemical"), ('Civil', "Civil"), ('Computer Science', "Computer Science"), ('Electrical',
                                                                                                                                                                 "Electrical"), ('Electronics', "Electronics"), ('Mechanical', "Mechanical"), ('Metallurgical', "Metallurgical"), ('Mining', "Mining"), ('Pharmaceutical', "Pharmaceutical"))

    name = serializers.CharField(max_length=200)
    branch = serializers.ChoiceField(choices=BRANCH)
    course = serializers.ChoiceField(choices=COURSE)
    year = serializers.ChoiceField(choices=YEAR)
    type_of_complaint = serializers.ChoiceField(choices=TYPE)
    description = serializers.CharField(max_length=4000)
    drive_link = serializers.URLField(
        max_length=400, allow_blank=True, required=False)

    def save(self):
        """
        Takes the validated data, creates a new grievance object and returns it.
        """
        name = self.validated_data.get('name')
        branch = self.validated_data.get('branch')
        course = self.validated_data.get('course')
        year = self.validated_data.get('year')
        type_of_complaint = self.validated_data.get('type_of_complaint')
        description = self.validated_data.get('description')
        drive_link = self.validated_data.get('drive_link', '')
        user = self.context["request"].user

        complaint = Complaint.objects.create(
            user=user, name=name, branch=branch, course=course,
            year=year, type_of_complaint=type_of_complaint,
            description=description, drive_link=drive_link)
        complaint.save()
        return complaint


class CountGrievanceSerializer(serializers.Serializer):
    def get_count(self):
        """
        Returns the count of closed, registered and pending grievances.
        """
        user = self.context["request"].user
        user_complaints = Complaint.objects.filter(user=user)
        closed_complaints = user_complaints.filter(status=1)
        registered_complaints = user_complaints.filter(status=2)
        pending_complaints = user_complaints.filter(status=3)

        return {
            "closed": closed_complaints.count(),
            "registered": registered_complaints.count(),
            "pending": pending_complaints.count()
        }


class GrievanceDetailSerializer(serializers.Serializer):
    STATUS = ((1, 'Closed'), (2, 'Registered'), (3, 'Pending'))

    def get_details(self, status):
        """
        Returns an array consisting of grievances created by the user
        having status same as the given status.
        """
        user = self.context["request"].user
        user_complaints = Complaint.objects.filter(user=user)
        detailed_complaints = user_complaints.filter(status=status).all()
        return detailed_complaints


class GrievanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complaint
        fields = ('id', 'name', 'branch', 'course', 'year', 'type_of_complaint',
                  'description', 'drive_link', 'status')
