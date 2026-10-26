
from database import get_db_connection


def migrate_hospital_database():
    new_columns = {
        "hospital_name": "TEXT",
        "department": "TEXT",
        "location": "TEXT",
    }

    with get_db_connection() as connection:
        existing_columns = {
            row["name"]
            for row in connection.execute(
                "PRAGMA table_info(contacts)"
            ).fetchall()
        }

        if not existing_columns:
            raise RuntimeError(
                "Contacts table not found. Migration stopped."
            )

        for column_name, column_type in new_columns.items():
            if column_name not in existing_columns:
                connection.execute(
                    f"ALTER TABLE contacts "
                    f"ADD COLUMN {column_name} {column_type}"
                )
                print(f"Added column: {column_name}")
            else:
                print(f"Already exists: {column_name}")

        connection.commit()

    print("Hospital database migration completed!")


if __name__ == "__main__":
    migrate_hospital_database()
