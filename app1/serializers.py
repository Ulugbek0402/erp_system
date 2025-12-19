from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Category, News, Commit

User = get_user_model()


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(write_only=True, required=False, allow_blank=True)

    is_admin = serializers.BooleanField(required=False)
    is_staff = serializers.BooleanField(required=False)
    is_manager = serializers.BooleanField(required=False)

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)

        for k, v in validated_data.items():
            setattr(instance, k, v)

        if password is not None and password != "":
            instance.set_password(password)

        instance.save()
        return instance


class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=100)

    def create(self, validated_data):
        return Category.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.save()
        return instance


class NewsSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=100)
    content = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    created = serializers.DateTimeField(read_only=True)
    updated = serializers.DateTimeField(read_only=True)
    photo = serializers.ImageField(required=False, allow_null=True)
    bool = serializers.BooleanField(required=False)
    views = serializers.IntegerField(required=False)
    category_id = serializers.IntegerField()

    def create(self, validated_data):
        category_id = validated_data.pop("category_id")

        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            raise serializers.ValidationError({"category_id": "Category topilmadi"})

        return News.objects.create(category=category, **validated_data)

    def update(self, instance, validated_data):
        if "category_id" in validated_data:
            category_id = validated_data.pop("category_id")
            try:
                category = Category.objects.get(id=category_id)
            except Category.DoesNotExist:
                raise serializers.ValidationError({"category_id": "Category topilmadi"})
            instance.category = category

        for k, v in validated_data.items():
            setattr(instance, k, v)

        instance.save()
        return instance


class CommitSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)

    user = serializers.CharField(source="user.username", read_only=True)

    news_id = serializers.IntegerField()
    text = serializers.CharField()
    created_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        request = self.context["request"]
        news_id = validated_data["news_id"]
        text = validated_data["text"]

        try:
            news = News.objects.get(id=news_id)
        except News.DoesNotExist:
            raise serializers.ValidationError({"news_id": "News topilmadi"})

        return Commit.objects.create(user=request.user, news=news, text=text)

    def update(self, instance, validated_data):
        if "news_id" in validated_data:
            try:
                instance.news = News.objects.get(id=validated_data["news_id"])
            except News.DoesNotExist:
                raise serializers.ValidationError({"news_id": "News topilmadi"})

        if "text" in validated_data:
            instance.text = validated_data["text"]

        instance.save()
        return instance

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()