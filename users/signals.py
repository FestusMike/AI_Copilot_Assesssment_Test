from django.db.models.signals import post_save
from django.dispatch import receiver
from faker import Faker
from users.models import UserAccount
from jobs.models import JobRecommendation

fake = Faker()


@receiver(post_save, sender=UserAccount)
def generate_recommendations(sender, instance, **kwargs):
    user_skills = instance.get_skills_list
    if not user_skills:
        return

    JobRecommendation.objects.filter(user=instance).delete()

    recommendations = []
    for _ in range(5):
        skill = fake.random_element(user_skills)
        recommendations.append(
            JobRecommendation(
                user=instance,
                job_title=f"{skill.capitalize()} {fake.job()}",
                company_name=fake.company(),
                job_url=fake.url(),
            )
        )

    JobRecommendation.objects.bulk_create(recommendations)
