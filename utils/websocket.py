from asgiref.sync import async_to_sync
from channels import DEFAULT_CHANNEL_LAYER
from channels.layers import get_channel_layer

def broadcast(group_name, function_name, event, alias=None):
    """
    :param group_name: name of a group registered with Consumer().channel_layer.group_add(<group_name>)
    :param function_name: name of a function registered in Consumer which group added
    :param alias:  alias of a channel layer
    :return:
    """
    channel_layer = get_channel_layer(alias=alias or DEFAULT_CHANNEL_LAYER)
    async_to_sync(channel_layer.group_send)(group_name, {'type': function_name, 'event': event})


