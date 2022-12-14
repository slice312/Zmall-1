import json

from rest_framework import serializers

from user.models import CustomUser
from advert.utils import connect_to_redis
from advert.models import (
    Advert,
    AdvertContact,
    AdvertImage,
    Category,
    SubCategory,
    City,
    AdvertReport,
    Promote,
    FeedbackMessage,
    PrivacyPolicy,
)


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = "__all__"


class AdvertContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvertContact
        fields = ("phone_number",)


class AdvertImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvertImage
        fields = ["image"]


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("id", "first_name", "last_name")


class AdvertCreateSerializer(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField(
        slug_field="id", queryset=CustomUser.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field="id", queryset=Category.objects.all()
    )
    sub_category = serializers.SlugRelatedField(
        slug_field="id", queryset=SubCategory.objects.all()
    )
    promote = serializers.SlugRelatedField(
        slug_field="types", queryset=Promote.objects.all(), allow_null=True
    )
    city = serializers.SlugRelatedField(slug_field="id", queryset=City.objects.all())

    class Meta:
        model = Advert

        exclude = ("created_date", "views")


class AdvertListSerializer(serializers.ModelSerializer):
    promote = serializers.SlugRelatedField(
        slug_field="types", queryset=Promote.objects.all()
    )
    sub_category = serializers.SlugRelatedField(slug_field="id", read_only=True)
    advert_contact = AdvertContactSerializer(many=True)
    advert_image_count = serializers.IntegerField(
        source="advert_image.count", read_only=True
    )
    advert_image = AdvertImageSerializer(read_only=True, many=True)
    city = serializers.SlugRelatedField(slug_field="id", queryset=City.objects.all())

    class Meta:
        model = Advert
        fields = (
            "id",
            "name",
            "sub_category",
            "start_price",
            "end_price",
            "promote",
            "advert_image_count",
            "views",
            "city",
            "created_date",
            "description",
            "advert_contact",
            "advert_image"
        )


class AdvertDetailSerializer(serializers.ModelSerializer):
    promote = serializers.SlugRelatedField(
        slug_field="types", queryset=Promote.objects.all()
    )
    owner = CustomUserSerializer()
    advert_contact = AdvertContactSerializer(many=True)
    city = serializers.SlugRelatedField(slug_field="id", read_only=True)
    advert_image = AdvertImageSerializer(many=True)

    class Meta:
        model = Advert
        fields = "__all__"


class UserAdvertDetailSerializer(serializers.ModelSerializer):
    promote = serializers.SlugRelatedField(
        slug_field="types", queryset=Promote.objects.all()
    )
    owner = CustomUserSerializer()
    advert_contact = AdvertContactSerializer(many=True)
    city = serializers.SlugRelatedField(slug_field="name", read_only=True)
    advert_image = AdvertImageSerializer(many=True)
    contact_views = serializers.SerializerMethodField(source="get_contact_views", read_only=True)

    class Meta:
        model = Advert
        fields = "__all__"

    def get_contact_views(self, instance):
        view = connect_to_redis()
        redis_views = view.get(instance.id)
        ad_views = 0

        if redis_views is not None:
            redis_views = json.loads(redis_views.decode("utf-8"))
            ad_views = redis_views['views_counter']
        return ad_views


class AdvertReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvertReport
        fields = "__all__"
