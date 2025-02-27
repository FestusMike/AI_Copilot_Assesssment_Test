import factory
from users.models import UserAccount
from faker import Faker

fake = Faker()


class UserAccountFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserAccount

    email = factory.LazyAttribute(lambda _: fake.email())
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    skills = factory.LazyAttribute(lambda _: ", ".join(fake.words(nb=5)))
