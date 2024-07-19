from django.db.models.signals import post_save
from django.dispatch import receiver

from .custom_storage import FunnelStepThumbnailImageStorage, MediaStorage
from .models import (
    FunnelStep,
    SalesFunnelOwner,
    get_image_filename,
)


@receiver(post_save, sender=SalesFunnelOwner)
def upload_image_to_s3(sender, instance, **kwargs):
    # Check if the instance has an image field and if it has changed
    if hasattr(instance, "image") and instance.image and instance.image.file:
        # Get the image file and its name
        image_file = instance.image.file
        image_name = instance.image.name

        # Check if the image has changed
        if image_file and hasattr(image_file, "file") and image_file.file:
            # Set the file name using your custom naming convention
            new_image_name = get_image_filename(instance, image_name)

            # Save the new image file to S3
            storage = MediaStorage()
            storage.save(new_image_name, image_file)

            # Update the instance with the new image URL
            instance.image.name = new_image_name
            instance.save()


@receiver(post_save, sender=FunnelStep)
def upload_funnel_thumbnail_image_to_s3(sender, instance, **kwargs):
    # Check if the instance has an image field and if it has changed
    if hasattr(instance, "image") and instance.image and instance.image.file:
        # Get the image file and its name
        image_file = instance.image.file
        image_name = instance.image.name

        # Check if the image has changed
        if image_file and hasattr(image_file, "file") and image_file.file:
            # Save the new image file to S3
            storage = FunnelStepThumbnailImageStorage()
            storage.save(image_name, image_file)

            # Update the instance with the new image URL
            instance.image.name = image_name
            instance.save()
