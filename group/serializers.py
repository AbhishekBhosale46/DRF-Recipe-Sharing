from rest_framework import serializers
from core.models import Group

class GroupSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField('get_owner', read_only=True)

    class Meta:
        model = Group
        fields = ['id', 'created_at', 'name', 'description', 'owner']
        read_only_fields = ['id', 'owner', 'created_at']

    def get_owner(self, group_obj):
        return group_obj.owner.name