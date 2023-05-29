import csv
import psycopg2

from testTask.models import Location


# Connect to the PostgreSQL database
def import_data_from_csv():
    with open('uszips.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Create a new Location object and set the attributes from the CSV row
            location = Location(
                zip=row["zip"],
                lat = row["lat"],
                lng = row["lng"],
                city = row["city"],
                state = row["state_name"],
            )
            # Save the Location object to the database
            location.save()

if __name__ == '__main__':
    import_data_from_csv()
