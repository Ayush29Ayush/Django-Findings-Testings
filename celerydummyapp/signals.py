from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django_celery_beat.models import PeriodicTask, IntervalSchedule

@receiver(post_migrate)
def create_periodic_task(sender, **kwargs):
    if not PeriodicTask.objects.filter(name='Say Hello Every Minute').exists():
        schedule, created = IntervalSchedule.objects.get_or_create(every=1, period=IntervalSchedule.MINUTES)
        PeriodicTask.objects.create(
            interval=schedule,
            name='Say Hello Every Minute',
            task='celerydummyapp.tasks.print_hello',
        )
