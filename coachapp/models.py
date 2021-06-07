from django.db import models


class CoachNote(models.Model):
    coach = models.ForeignKey(
        "app.User", related_name="coach", on_delete=models.SET_NULL,null=True
    )

    note = models.TextField()
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.id)
