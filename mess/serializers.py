from rest_framework import serializers
from .models import Bill, Mess, Hostel
from authentication.models import UserProfile


class HostelListSerializer(serializers.ModelSerializer):
    """
    Serializer for hostel list view.
    """
    class Meta:
        model = Hostel
        fields = ('id', 'name',)


class MessDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for mess list and detail view.
    """
    class Meta:
        model = Mess
        fields = ('id', 'name', 'menu',)


class MessBillSerializer(serializers.Serializer):
    """
    Serializer for showing the billing of individual students.
    """

    def validate(self, data):
        """
        Checks if the current user is subscribed to the mess
        with given id. Raises error if not subscribed.
        """
        mess_id = self.context['mess_id']
        mess = Mess.objects.filter(id=mess_id)
        if not mess:
            raise serializers.ValidationError(
                'Mess with given id does not exist.')

        mess = mess.first()
        month = self.context['month']
        user = self.context['request'].user
        user_profile = UserProfile.objects.filter(user=user).first()

        bill = Bill.objects.filter(
            user_profile=user_profile, mess=mess, month=month)
        if not bill:
            raise serializers.ValidationError(
                'Bill details not found for the student with given mess and month.')

        data['bill'] = bill.first()
        return data

    def get_bill_details(self):
        """
        Fetches the billing details of the current user
        and returns the serialized bill details.
        """
        data = self.validated_data
        bill = data.get('bill')
        serialized_bill = BillSerializer(bill)
        return serialized_bill.data


class BillSerializer(serializers.ModelSerializer):
    """
    Helper serializer for serializing the bill objects.
    """
    name = serializers.CharField(source='user_profile.name')
    mess = serializers.CharField(source='mess.name')

    class Meta:
        model = Bill
        fields = ('name', 'mess', 'monthly_bill', 'extra_charges', 'month',)
