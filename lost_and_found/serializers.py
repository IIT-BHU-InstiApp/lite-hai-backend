from rest_framework import serializers
from .models import LostAndFound


class CreateLostAndFoundSerializer(serializers.Serializer):
    TYPE = (('Security', "Security"), ('Health&Hygiene', "Health&Hygiene"),
            ('HostelMess', "HostelMess"), ('Academics', "Academics"),
            ('Council', "Council"), ('Others', "Others"))
    YEAR = (('1st', "1st"), ('2nd', "2nd"),
            ('3rd', "3rd"), ('4th', "4th"), ('5th', "5th"))
    COURSE = (('B.Tech', "B.Tech"), ('IDD', "IDD"), ('M.Tech', "M.Tech"))
    BRANCH = (('Architecture', "Architecture"), ('Ceramic', "Ceramic"),
              ('Chemical', "Chemical"), ('Civil',
                                         "Civil"), ('Computer Science', "Computer Science"),
              ('Electrical', "Electrical"), ('Electronics',
                                             "Electronics"), ('Mechanical', "Mechanical"),
              ('Metallurgical', "Metallurgical"), ('Mining', "Mining"), ('Pharmaceutical', "Pharmaceutical"))

    name = serializers.CharField(max_length=200)
    branch = serializers.ChoiceField(choices=BRANCH)
    course = serializers.ChoiceField(choices=COURSE)
    year = serializers.ChoiceField(choices=YEAR)
    type_of_lost_and_found = serializers.ChoiceField(choices=TYPE)
    description = serializers.CharField(max_length=4000)

    def save(self):
        """
        Takes the validated data, creates a new lost and found object and returns it.
        """
        data = self.validated_data
        name = data.get('name')
        branch = data.get('branch')
        course = data.get('course')
        year = data.get('year')
        type_of_lost_and_found = data.get(
            'type_of_lost_and_found')
        description = data.get('description')
        user = self.context["request"].user

        # pylint: disable=no-member
        lost_and_found = LostAndFound.objects.create(
            user=user, name=name, branch=branch, course=course,
            year=year, type_of_lost_and_found=type_of_lost_and_found,
            description=description)
        lost_and_found.save()
        return lost_and_found


class CountLostAndFoundSerializer(serializers.Serializer):
    def get_count(self):
        """
        Returns the count of closed, registered and pending lost and found objects.
        """
        user = self.context["request"].user
        # pylint: disable=no-member
        user_lost_and_found = LostAndFound.objects.filter(user=user)
        closed_lost_and_found = user_lost_and_found.filter(status=1)
        registered_lost_and_found = user_lost_and_found.filter(status=2)
        pending_lost_and_found = user_lost_and_found.filter(status=3)

        return {
            "closed": closed_lost_and_found.count(),
            "registered": registered_lost_and_found.count(),
            "pending": pending_lost_and_found.count()
        }


class LostAndFoundDetailSerializer(serializers.Serializer):
    STATUS = ((1, 'Closed'), (2, 'Registered'), (3, 'Pending'))

    def get_details(self, status):
        """
        Returns an array consisting of lost and found objects created by the user
        having status same as the given status.
        """
        user = self.context["request"].user
        # pylint: disable=no-member
        user_lost_and_found = LostAndFound.objects.filter(user=user)
        detailed_lost_and_found = user_lost_and_found.filter(
            status=status).all()
        return detailed_lost_and_found


class LostAndFoundSerializer(serializers.ModelSerializer):
    class Meta:
        model = LostAndFound
        fields = ('id', 'name', 'branch', 'course', 'year', 'type_of_lost_and_found',
                  'description', 'status')
