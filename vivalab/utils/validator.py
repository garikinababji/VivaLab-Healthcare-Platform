class Validator:

    REQUIRED_FIELDS = [
        "patient_id",
        "first_name",
        "last_name",
        "gender",
        "date_of_birth"
    ]

    @staticmethod
    def validate(record):

        errors = []

        for field in Validator.REQUIRED_FIELDS:

            if field not in record:
                errors.append(f"{field} is missing")

            elif record[field] in ("", None):
                errors.append(f"{field} is empty")

        return errors