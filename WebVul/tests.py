from django.test import TestCase

# Create your tests here.
from WebVul.models import LoginUsers

true_username = LoginUsers.objects.get(user_name="zrl")
print(true_username)