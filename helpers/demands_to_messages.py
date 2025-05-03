from models.Demand import Demand
from models.User import User


def demands_to_messages(demands:list[Demand]) -> list[dict]:
    """
    Convert a list of demands into a list of messages.

    Args:
        demands (list): A list of demand dictionaries.

    Returns:
        list: A list of message dictionaries.
    """
    messages = []
    for demand in demands:
        user:User = User.query.get(demand.user_id)
        message = {
            "role": "user",
            "content": f"User {user.username} is looking for a trip with the following preferences: "
                       f"Wants to go to the mountain: {demand.mountain}, wants to go to the beach: {demand.beach}, "
                       f"wants to be in a big City: {demand.big_city}, wants to be in a village: {demand.village}, "
                       f"maximum price: {demand.price}, extra demands: {demand.description}"
        }
        messages.append(message)
    return messages