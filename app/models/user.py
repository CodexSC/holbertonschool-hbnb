import re
from app.models.base_model import BaseModel


class User(BaseModel):
    """
    Represents a user of the HBnB platform.

    Attributes:
        first_name (str): Required, max 50 characters.
        last_name  (str): Required, max 50 characters.
        email      (str): Required, must be a valid email format, must be unique.
        is_admin   (bool): Whether the user has admin rights. Defaults to False.
    """

    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()
        self.first_name = first_name   # uses the setter -> validates
        self.last_name = last_name     # uses the setter -> validates
        self.email = email             # uses the setter -> validates
        self.is_admin = is_admin

    # ----------------------------------------------------------------
    # first_name: required, string, max 50 characters
    # ----------------------------------------------------------------
    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        if not value or not isinstance(value, str):
            raise ValueError("first_name is required and must be a string.")
        if len(value) > 50:
            raise ValueError("first_name must not exceed 50 characters.")
        self._first_name = value

    # ----------------------------------------------------------------
    # last_name: required, string, max 50 characters
    # ----------------------------------------------------------------
    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        if not value or not isinstance(value, str):
            raise ValueError("last_name is required and must be a string.")
        if len(value) > 50:
            raise ValueError("last_name must not exceed 50 characters.")
        self._last_name = value

    # ----------------------------------------------------------------
    # email: required, must follow standard email format
    # ----------------------------------------------------------------
    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if not value or not isinstance(value, str):
            raise ValueError("email is required.")
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(pattern, value):
            raise ValueError("email must be a valid email address (e.g. user@example.com).")
        self._email = value

    # ----------------------------------------------------------------
    # to_dict: include all user fields
    # ----------------------------------------------------------------
    def to_dict(self):
        data = super().to_dict()
        data.update({
            'first_name': self.first_name,
            'last_name':  self.last_name,
            'email':      self.email,
            'is_admin':   self.is_admin
        })
        return data
