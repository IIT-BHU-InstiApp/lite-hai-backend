from datetime import date
from rest_framework import serializers
from .models import NoticeBoard


class NoticeBoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = NoticeBoard
        fields = ('name', 'description', 'date', 'link', 'ping', 'upvote', 'downvote')
