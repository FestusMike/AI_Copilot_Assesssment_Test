import factory
from jobs.models import ResumeFeedback
from .users_factory import UserAccountFactory
from faker import Faker

fake = Faker()


class ResumeFeedbackFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ResumeFeedback

    user = factory.SubFactory(UserAccountFactory)
    resume_text = factory.Faker("text", max_nb_chars=500)
    feedback = factory.LazyAttribute(
        lambda _: {"suggestions": [fake.sentence() for _ in range(3)]}
    )
