from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

PATIENT_NAMES = [
    "Aarav", "Priya", "Rohan", "Aanya", "Vikram",
    "Meera", "Arjun", "Kavya", "Suresh", "Divya",
]

class Command(BaseCommand):
    help = "Deletes all seeded patients"

    def handle(self, *args, **kwargs):
        self.stdout.write("\n🗑️  Deleting seeded patients...\n")
        for name in PATIENT_NAMES:
            deleted, _ = User.objects.filter(username=name).delete()
            if deleted:
                self.stdout.write(self.style.SUCCESS(f"  ✓ Deleted: {name}"))
            else:
                self.stdout.write(f"  → Not found: {name}")
        self.stdout.write(self.style.SUCCESS("\n✅ Done!\n"))