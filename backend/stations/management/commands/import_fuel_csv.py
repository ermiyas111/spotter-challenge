from django.core.management.base import BaseCommand, CommandError

from stations.services.csv_importer import import_fuel_csv


class Command(BaseCommand):
    help = "Import fuel station data from a CSV file"

    def add_arguments(self, parser):
        parser.add_argument("csv_path", type=str)

    def handle(self, *args, **options):
        csv_path = options["csv_path"]
        try:
            data_import = import_fuel_csv(csv_path)
        except Exception as exc:
            raise CommandError(str(exc)) from exc

        self.stdout.write(
            self.style.SUCCESS(
                f"Import completed: {data_import.id} (invalid rows: {data_import.invalid_row_count})"
            )
        )
