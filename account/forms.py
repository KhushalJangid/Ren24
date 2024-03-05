from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate,login

class LoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email")
    # def clean(self):
    #     username = self.cleaned_data.get("username")
    #     password = self.cleaned_data.get("password")

    #     if username is not None and password:
    #         self.user_cache = authenticate(
    #             self.request, username=username, password=password
    #         )
    #         if self.user_cache is None:
    #             raise self.get_invalid_login_error()
    #         else:
    #             self.confirm_login_allowed(self.user_cache)
    #     # self.cleaned_data["username"] = self.user_cache.id
    #     # print(self.cleaned_data)
    #     return self.cleaned_data

    # def confirm_login_allowed(self, user):
    #     """
    #     Controls whether the given User may log in. This is a policy setting,
    #     independent of end-user authentication. This default behavior is to
    #     allow login by active users, and reject login by inactive users.

    #     If the given user cannot log in, this method should raise a
    #     ``ValidationError``.

    #     If the given user may log in, this method should return None.
    #     """
    #     if not user.is_active:
    #         raise forms.ValidationError(
    #             self.error_messages["inactive"],
    #             code="inactive",
    #         )
            
    # def get_invalid_login_error(self):
    #     return forms.ValidationError(
    #         self.error_messages["invalid_login"],
    #         code="invalid_login",
    #         params={"username": self.username_field.verbose_name},
    #     )
    
