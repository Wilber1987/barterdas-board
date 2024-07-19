from barter_auth.models import UnilevelNetwork

#region user helpers
def add_user_to_network(user):
    user_loop = user
    user_in_network = user
    user_trought = user.referred_by
    index = 1
    uniList = []

    while user_loop.referred_by != None and user_loop.referred_by != user_loop:
        uniList.append(UnilevelNetwork(user=user_loop.referred_by,user_in_network=user_in_network,in_network_through=user_trought,level=index))
        user_loop = user_loop.referred_by
        index = index + 1

    UnilevelNetwork.objects.bulk_create(uniList)
    

def build_user_unilevel_network_data(user):
    user_data = {
        'image': '',
        'name': f'{user.first_name} {user.last_name}',
        'title': '',
    }
    
    children = UnilevelNetwork.objects.filter(in_network_through=user)
    
    user_data['children'] = [build_user_unilevel_network_data(child.user_in_network) for child in children]
    
    return user_data
#endregion