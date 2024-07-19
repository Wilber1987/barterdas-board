from barter_auth.models import BarterUser, UnilevelNetwork


def add_user_to_network(user: BarterUser):
    user_loop = user
    user_in_network = user
    user_trought = user.referred_by
    index = 1
    uniList = []

    while user_loop.referred_by is not None and user_loop.referred_by != user_loop:
        uniList.append(
            UnilevelNetwork(
                user=user_loop.referred_by,
                user_in_network=user_in_network,
                in_network_through=user_trought,
                level=index,
            )
        )
        user_loop = user_loop.referred_by
        index = index + 1

    UnilevelNetwork.objects.bulk_create(uniList)