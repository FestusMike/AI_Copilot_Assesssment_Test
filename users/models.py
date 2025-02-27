from django.db import models
from django.contrib.auth import models as dj_models
from includes.helpers import models as helper_models
from users.managers import CustomUserManager


class UserAccount(
    dj_models.AbstractUser,
    helper_models.PrimaryKeyMixin,
    helper_models.DateHistoryMixin,
):
    username = None
    email = models.EmailField(
        verbose_name=("email address"),
        unique=True,
        blank=False,
        null=False,
        help_text=("The email address of the user"),
        error_messages={
            "unique": ("User with that email already exists."),
        },
    )
    skills = models.TextField(
        blank=True, help_text="Comma-separated skills for job recommendations"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = CustomUserManager()

    @property
    def get_skills_list(self):
        return [
            skill.strip().lower() for skill in self.skills.split(",") if skill.strip()
        ]
