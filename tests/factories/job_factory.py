import factory
from .users_factory import UserAccountFactory
from jobs.models import JobApplication
from django.utils import timezone
from jobs.enums import JobApplicationStatus
from faker import Faker

fake = Faker()


class JobApplicationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = JobApplication

    user = factory.SubFactory(UserAccountFactory)
    job_title = factory.Faker("job")
    company_name = factory.Faker("company")
    status = factory.Iterator(JobApplicationStatus.values)
    applied_date = factory.LazyFunction(timezone.now)
    notes = factory.Faker("text")
