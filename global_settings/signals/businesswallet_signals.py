from django.dispatch import receiver
from django.db.models.signals import post_save

from global_settings.custom_storage import QRCodeStorage
from global_settings.models import (
    BusinessWallet,
    get_qr_filename
)

@receiver(post_save, sender=BusinessWallet)
def upload_businesswallet_qrcode_image_to_s3(sender, instance, **kwargs):
    # Check if the instance has an qr_code field and if it has changed
    if hasattr(instance, 'image') and instance.image and instance.image.file:
        # Get the image file and its name
        image_file = instance.image.file
        image_name = instance.image.name

        # Check if the image has changed
        if image_file and hasattr(image_file, 'file') and image_file.file:
            # Set the file name using your custom naming convention

            # Save the new image file to S3
            storage = QRCodeStorage()
            storage.save(image_name, image_file)

            # Update the instance with the new image URL
            instance.image.name = image_name
            instance.save()