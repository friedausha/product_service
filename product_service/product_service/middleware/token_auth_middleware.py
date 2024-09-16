import requests
import json
from django.conf import settings
from django.http import HttpResponse

AUTH_ERROR_MESSAGE = {'detail': 'Authentication credentials were not provided.'}
INVALID_TOKEN_MESSAGE = {'detail': 'Invalid token.'}


def to_json_response(data, status=200):
    # Helper function to return a JSON response
    return HttpResponse(
        json.dumps(data),
        content_type='application/json',
        status=status
    )


class TokenAuthMiddleware:
    def process_request(self, request):
        # Initialize custom message storage for the request
        request.custom_messages = []

        # Check if the request path is for the products API
        if request.path.startswith('/api/products/'):
            auth_token = request.META.get('HTTP_AUTHORIZATION', None)

            # If no auth token is provided, add a custom message and return a 401 response
            if not auth_token:
                self.add_message(request, 'error', AUTH_ERROR_MESSAGE['detail'])
                return to_json_response({'messages': self.get_messages(request)}, status=401)

            # If the token is invalid, add a custom message and return a 401 response
            if not self.validate_token(auth_token):
                self.add_message(request,  'error', INVALID_TOKEN_MESSAGE['detail'])
                return to_json_response({'messages': self.get_messages(request)}, status=401)

    def validate_token(self, token):
        VALIDATE_TOKEN_URL = settings.USER_SERVICE + 'api/token/verify'
        token_validation_response = requests.post(VALIDATE_TOKEN_URL,
            headers={'Authorization': token}
        )
        print (token_validation_response.json())
        return token_validation_response.status_code == 200

    def process_response(self, request, response):
        # Handle messages in the response if it is a JSON response
        print (response)
        if isinstance(response, HttpResponse) and response['Content-Type'] == 'application/json':
            try:
                response_data = json.loads(response.content)
            except ValueError:
                response_data = {}

            # Add custom messages to the response data
            response_data['messages'] = self.get_messages(request)
            return to_json_response(response_data, status=response.status_code)

        # If response is a dict, ensure it's returned as JSON with messages
        if isinstance(response, dict):
            response['messages'] = self.get_messages(request)
            return to_json_response(response)
        return response

    def add_message(self, request, level, message):
        # Add a custom message to the request's message storage
        request.custom_messages.append({'level': level, 'message': message})

    def get_messages(self, request):
        # Return all custom messages from the request
        return getattr(request, 'custom_messages', [])
