from datetime import datetime, timedelta
from io import BytesIO
import pytz
from django.core.files.base import ContentFile
from django.urls import reverse
from rest_framework import serializers
from core.models import Images
from PIL import Image


def modify_img(image, height: int, width: int):
    pil_image = Image.open(image)
    pil_image = pil_image.resize((height, width), resample=Image.BICUBIC)
    buffer = BytesIO()
    pil_image.save(buffer, format='PNG')
    buffer.seek(0)
    image_file = ContentFile(buffer.getvalue(), name=image.name)
    return image_file


class SmallImageSerialzier(serializers.ModelSerializer):
    title = serializers.CharField()
    image = serializers.ImageField()
    expired_time = serializers.IntegerField(required=False, default=None)

    def validate_expired_time(self, obj):
        if obj is None:
            return None
        if self.context['request'].user.plan in ["ROOT", "ENTERPRISE"]:
            if obj < 300 or obj > 30000:
                raise serializers.ValidationError("Expired_at must be number between 300 and 30000")
            expired_time = datetime.now(pytz.timezone('UTC')) + timedelta(seconds=obj)
            return expired_time
        raise serializers.ValidationError("You have no permission to use expired_time")




    def create(self, validated_data):
        request = self.context.get("request")
        image = modify_img(validated_data["image"], 200, 200)
        image_upload = Images.objects.create(title=validated_data['title'], image=image,
                                             uploaded_by=request.user, resolution='200x200',
                                             expired_at=validated_data['expired_time'])
        return image_upload

    class Meta:
        model = Images
        fields = ("image", "title", "expired_time")


class MediumImageSerialzier(serializers.ModelSerializer):
    title = serializers.CharField()
    image = serializers.ImageField()
    expired_time = serializers.IntegerField(required=False, default=None)

    def validate_expired_time(self, obj):
        if obj is None:
            return None
        if self.context['request'].user.plan in ["ROOT", "ENTERPRISE"]:
            if obj < 300 or obj > 30000:
                raise serializers.ValidationError("Expired_time must be number between 300 and 30000")
            expired_time = datetime.now(pytz.timezone('UTC')) + timedelta(seconds=obj)
            return expired_time
        raise serializers.ValidationError("You have no permission to use expired_time")

    def create(self, validated_data):
        request = self.context.get("request")
        image = modify_img(validated_data["image"], 400, 400)
        image_upload = Images.objects.create(title=validated_data['title'], image=image,
                                             uploaded_by=request.user, resolution='400x400',
                                             expired_at=validated_data['expired_time'])
        return image_upload

    class Meta:
        model = Images
        fields = ("image", "title", "expired_time")


class OriginalImageSerialzier(serializers.ModelSerializer):
    title = serializers.CharField()
    image = serializers.ImageField()
    expired_time = serializers.IntegerField(required=False, default=None)

    def validate_expired_time(self, obj):
        if obj is None:
            return None
        if self.context['request'].user.plan in ["ROOT", "ENTERPRISE"]:
            if obj < 300 or obj > 30000:
                raise serializers.ValidationError("Expired_time must be number between 300 and 30000")
            expired_time = datetime.now(pytz.timezone('UTC')) + timedelta(seconds=obj)
            return expired_time
        raise serializers.ValidationError("You have no permission to use expired_time")

    def create(self, validated_data):
        request = self.context.get("request")
        img = Image.open(validated_data['image'])
        image = modify_img(validated_data['image'], img.height, img.width)
        image_upload = Images.objects.create(title=validated_data['title'], image=image,
                                             uploaded_by=request.user, resolution=f'{img.height}x{img.width}',
                                             expired_at=validated_data['expired_time'])
        return image_upload

    class Meta:
        model = Images
        fields = ("image", "title", "expired_time")


class ListImageSerializer(serializers.ModelSerializer):
    link = serializers.SerializerMethodField(read_only=True)

    def get_link(self,obj):
        request = self.context.get('request')
        scheme = 'https' if request.is_secure() else 'http'
        host = request.get_host()
        return f"{scheme}://{host}" + reverse('img_view',kwargs={'id': obj.id})


    class Meta:
        model = Images
        fields = ('title', 'link', 'resolution', 'create_at','expired_at')


class CustomImageSerialzier(serializers.Serializer):
    title = serializers.CharField()
    height = serializers.IntegerField()
    width = serializers.IntegerField()
    image = serializers.ImageField()
    expired_time = serializers.IntegerField(required=False, default=None)

    def validate_expired_time(self, obj):
        if obj is None:
            return None
        if self.context['request'].user.plan in ["ROOT", "ENTERPRISE"]:
            if obj < 300 or obj > 30000:
                raise serializers.ValidationError("Expired_time must be number between 300 and 30000")
            expired_time = datetime.now(pytz.timezone('UTC')) + timedelta(seconds=obj)
            return expired_time
        raise serializers.ValidationError("You have no permission to use expired_time")

    def create(self, validated_data):
        request = self.context.get("request")
        image_file = modify_img(validated_data["image"], validated_data["height"], validated_data["width"])

        image_upload = Images.objects.create(title=validated_data['title'], image=image_file,
                                             uploaded_by=request.user,
                                             resolution=f'{validated_data["height"]}x{validated_data["width"]}',
                                             expired_at=validated_data['expired_time'])
        return image_upload


class ImagaViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = ('image',)


