from django.db.models.signals import post_save
from django.dispatch import receiver
from barter_auth.models import BarterUser
from global_settings.models import RootBarterUser
from barter_auth.model_utils.barteruser_utils import add_user_to_network
from transactions.utils.balance_utils import generate_initial_balance_instance


@receiver(post_save, sender=BarterUser)
def create_related_barteruser_model_instances(
    sender, instance: BarterUser, created, **kwargs
):
    if created:
        # Create unilevel network instances
        if instance.referred_by is not None:
            add_user_to_network(instance)
        else:
            latest_root_user = (
                RootBarterUser.objects.filter(enabled=True).order_by("-pk").first()
            )

            if latest_root_user is not None:
                instance.referred_by = latest_root_user.user

                add_user_to_network(instance)
                instance.save()

        # Create an user's initial balance
        new_balance_instance = generate_initial_balance_instance(instance)
        new_balance_instance.save()