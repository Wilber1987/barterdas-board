from rest_framework import serializers
from sales_funnel.models import SalesFunnelOwner, NewsletterSubscription, FunnelStep, get_image_filename
from sales_funnel.custom_storage import MediaStorage

class SalesFunnelOwnerSerializer(serializers.HyperlinkedModelSerializer):
    referral_link = serializers.CharField(source='user.referral_link')

    class Meta:
        model = SalesFunnelOwner
        fields = (
            # 'url',
            'id',
            'username',
            'display_name',
            'email',
            'whatsapp_phone_number',
            'facebook_account_url',
            'twitter_account_url',
            'custom_video_url',
            'profile_image',
            'referral_link'
        )
        read_only_fields = (
            'id',
            'referral_link',
        )

    def create(self, validated_data):
        if 'profile_image' in validated_data:
            image = validated_data.pop('profile_image')
        
        instance = SalesFunnelOwner.objects.create(**validated_data)

        if image is not None:

            # Use the S3Boto3Storage to handle the file upload
            storage = MediaStorage()
            new_image_name = get_image_filename(instance, image.name)
            path = f"{new_image_name}"
            storage.save(path, image)

            instance.profile_image.name = path
        instance.save()

        return instance
    
    def update(self, instance, validated_data):
        if 'profile_image' in validated_data:
            # Delete the old image file from S3
            storage = MediaStorage()
            # storage.delete(instance.image.name)

            # Upload the new image file to S3
            image = validated_data.pop('profile_image')
            new_image_name = get_image_filename(instance, image.name)
            path = f"{new_image_name}"
            storage.save(path, image)
            instance.profile_image.name = path

        instance.username = validated_data.get('username', instance.username)
        instance.display_name = validated_data.get('display_name', instance.display_name)
        instance.email = validated_data.get('email', instance.email)
        instance.whatsapp_phone_number = validated_data.get('whatsapp_phone_number', instance.whatsapp_phone_number)
        instance.facebook_account_url = validated_data.get('facebook_account_url', instance.facebook_account_url)
        instance.twitter_account_url = validated_data.get('twitter_account_url', instance.twitter_account_url)
        instance.custom_video_url = validated_data.get('custom_video_url', instance.custom_video_url)

        instance.save()
        return instance

class NewsletterSubscriptionSerializer(serializers.HyperlinkedModelSerializer):
    subscribed_to = serializers.SlugRelatedField(
        many=False,
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = NewsletterSubscription
        fields = (
            # 'url',
            'id',
            'subscribed_to',
            'subscriptor_email',
            'sent_emails',
            'created_at',
        )
        read_only_fields = (
            'subscribed_to',
            'sent_emails',
            'created_at',
        )

class FunnelStepSerializer(serializers.HyperlinkedModelSerializer):
    next_step = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='funnelstep-detail'
    )

    class Meta:
        model = FunnelStep
        fields = (
            'url',
            'pk',
            'step_number',
            'title',
            'youtube_video_url',
            'next_step',
            'thumbnail_image'
        )