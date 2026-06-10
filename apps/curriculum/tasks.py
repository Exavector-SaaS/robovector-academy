from celery import shared_task


@shared_task
def create_course_background(title, organization_id):
    from apps.curriculum.models import Course
    from apps.core.models import Organization

    org = Organization.objects.get(id=organization_id)

    Course.objects.create(title=title, organization=org)
