import factory
from jobs.models import JobRecommendation
from .users_factory import UserAccountFactory
from django.utils import timezone
from faker import Faker

fake = Faker()


class JobRecommendationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = JobRecommendation

    user = factory.SubFactory(UserAccountFactory)
    job_title = factory.Faker("job")
    company_name = factory.Faker("company")
    job_url = factory.Faker("url")
    posted_at = factory.LazyFunction(timezone.now)
