class UserSerializer(object):
    @staticmethod
    def to_dict(instance):
        # Check if instance is a dict, use 'get' for safe access
        if isinstance(instance, dict):
            return {
                "id": instance.get("id"),
                "username": instance.get("username"),
                "full_name": instance.get("full_name"),
                "email": instance.get("email"),
            }

        # Otherwise, assume it's an object with attributes
        return {
            "id": getattr(instance, "id", None),
            "username": getattr(instance, "username", None),
            "full_name": getattr(instance, "full_name", None),
            "email": getattr(instance, "email", None),
        }

    @staticmethod
    def from_dict(data):
        return {
            "id": data.get("id"),
            "username": data.get("username"),
            "full_name": data.get("full_name"),
            "email": data.get("email"),
            "password": data.get("password"),
        }
