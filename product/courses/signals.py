from django.db.models import Count
from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import Subscription
from courses.models import Group


@receiver(post_save, sender=Subscription)
def post_save_subscription(sender, instance: Subscription, created, **kwargs):
    """Распределение нового студента в группу курса."""
    if created:
        course = instance.course
        groups = (course.groups.annotate(student_count=Count('students')).
                  order_by('student_count'))

        if groups.exists():
            group = groups.first()
        else:
            group = Group.objects.create(
                course=course,
                title=f"Группа №{course.groups.count() + 1}"
            )

        group.students.add(instance.user)
        group.save()
