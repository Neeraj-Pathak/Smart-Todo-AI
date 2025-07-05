from django.db import models
from django.utils import timezone


class Category(models.Model):
    """
    Task categories / tags.
    `usage_count` increments automatically each time a task is created
    with this category (see Task.save()).
    """
    name = models.CharField(max_length=50, unique=True)
    usage_count = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class ContextEntry(models.Model):
    """
    Raw daily context captured from WhatsApp, email, notes, etc.
    `source_type` is a short code for quick filtering.
    """
    SOURCE_CHOICES = [
        ("WA", "WhatsApp"),
        ("EM", "Email"),
        ("NT", "Note"),
    ]

    content = models.TextField()
    source_type = models.CharField(max_length=2, choices=SOURCE_CHOICES)
    timestamp = models.DateTimeField(default=timezone.now)

    # Optional: AI‑processed metadata
    insights = models.JSONField(blank=True, null=True)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.get_source_type_display()} @ {self.timestamp:%Y‑%m‑%d %H:%M}"


class Task(models.Model):
    """
    Core task table with AI fields.
    """
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("done", "Done"),
    ]

    title = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    category = models.ForeignKey(
        Category, null=True, blank=True, on_delete=models.SET_NULL
    )
    priority_score = models.DecimalField(max_digits=4, decimal_places=2, default=5)
    deadline = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Link to context entries used to create / enhance this task (optional)
    context_used = models.ManyToManyField(ContextEntry, blank=True, related_name="tasks")

    class Meta:
        ordering = ["-priority_score", "deadline"]

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)

        # increment usage_count only on first save
        if is_new and self.category:
            Category.objects.filter(pk=self.category_id).update(
                usage_count=models.F("usage_count") + 1
            )

    def __str__(self):
        return self.title
