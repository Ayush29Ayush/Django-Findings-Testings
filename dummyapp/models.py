from django.db import models

class DummyModel(models.Model):
    num1 = models.IntegerField()
    num2 = models.IntegerField()
    sum = models.IntegerField(blank=True)

    def save(self, *args, **kwargs):
        self.sum = self.num1 + self.num2
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.num1} + {self.num2} = {self.sum}"

    class Meta:
        verbose_name = "Dummy Model"
        verbose_name_plural = "Dummy Models"