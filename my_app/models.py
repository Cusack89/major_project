from django.db import models
from django.contrib.auth.models import User

class BodyArea(models.Model):
    name = models.CharField(max_length=100)
    parent_area = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="sub_areas"
    )

    def __str__(self):
        return self.name


class PainType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Stretch(models.Model):
    name = models.CharField(max_length=150)
    stretch_type = models.CharField(max_length=100)
    description = models.TextField()
    cover_image_url = models.URLField(blank=True)
    difficulty_level = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Injury(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="injuries")
    location = models.ForeignKey(BodyArea, on_delete=models.CASCADE)
    pain_type = models.ForeignKey(PainType, on_delete=models.CASCADE)
    severity = models.IntegerField()
    date_occurred = models.DateField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.body_area} - {self.pain_type}"


class StretchMapping(models.Model):
    body_area = models.ForeignKey(BodyArea, on_delete=models.CASCADE)
    pain_type = models.ForeignKey(PainType, on_delete=models.CASCADE)
    stretch = models.ForeignKey(Stretch, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.body_area} + {self.pain_type} → {self.stretch}"



class SavedStretch(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="users_profile"
    )
    stretch = models.ForeignKey(Stretch, on_delete=models.CASCADE)
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "stretch")

    def __str__(self):
        return f"{self.user.username} saved {self.stretch.name}"
    

## ROUTINE MODELS 

class RoutineLabel(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Routine(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    difficulty = models.CharField(max_length=50, blank=True)
    cover_image_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    labels = models.ManyToManyField("RoutineLabel", blank=True)
    stretches = models.ManyToManyField("Stretch", through="RoutineStretch")

    saved_by = models.ManyToManyField(
        User,
        related_name="saved_routines",
        blank=True
    )

    def __str__(self):
        return self.title


class RoutineStretch(models.Model):
    routine = models.ForeignKey(Routine, on_delete=models.CASCADE)
    stretch = models.ForeignKey("Stretch", on_delete=models.CASCADE)
    order_number = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.routine} - {self.stretch}"
    
class SavedRoutine(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    routine = models.ForeignKey(Routine, on_delete=models.CASCADE)
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "routine")

    def __str__(self):
        return f"{self.user.username} saved {self.routine.title}"