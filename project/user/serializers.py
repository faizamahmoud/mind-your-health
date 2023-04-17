from rest_framework import serializers
from .models import JournalEntry, EndUser


class JournalEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = JournalEntry
        fields = ['id', 'author', 'description', 'date']

class EndUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = EndUser
        fields = ['first_name', 'last_name', 'email', 'password', 'weight']

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.set_password(validated_data.get('password', instance.password))
        instance.weight = validated_data.get('weight', instance.weight)
        instance.save()
        return instance
