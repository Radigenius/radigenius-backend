from django.core.exceptions import ValidationError


class ModelValidator:
    def __init__(self, instance, field_rules):
        """
        Initializes the validator with the model instance and validation rules.

        :param instance: The Django model instance to validate.
        :param field_rules: A dictionary where keys are field names and values are validation rules.
        """
        self.instance = instance
        self.field_rules = field_rules

    def validate(self):
        """
        Validates the fields of the instance based on the specified rules.
        Raises ValidationError with specific field errors if any validation fails.
        """
        errors = {}

        for field, rules in self.field_rules.items():
            value = getattr(self.instance, field, None)

            # Iterate through all rule keys and validate using the corresponding methods
            for rule, rule_value in rules.items():
                validate_method = getattr(self, f"validate_{rule}", None)
                if validate_method:
                    error = validate_method(field, value, rule_value)
                    if error:
                        errors[field] = error

        if errors:
            raise ValidationError(errors)

    # Validation methods
    def validate_required(self, field, value, required):
        if required and value in [None, "", []]:
            return "This field is required."
        return None

    def validate_type(self, field, value, expected_type):
        if value is not None and not isinstance(value, expected_type):
            return (
                f"Expected type {expected_type.__name__}, got {type(value).__name__}."
            )
        return None

    def validate_min(self, field, value, min_value):
        if value is not None and value < min_value:
            return f"Value must be at least {min_value}."
        return None

    def validate_max(self, field, value, max_value):
        if value is not None and value > max_value:
            return f"Value must be no greater than {max_value}."
        return None

    def validate_enforce_None(self, field, value, _):
        if value is not None:
            return "This field should be None"

    def validate_not_editable(self, field, value, _):
        # If the instance is new, or value is empty which perform as not changed,no validation is needed for immutability
        if not self.instance.parent or value in [None, "", []]:
            return None

        parent_instance = (
            self.instance.__class__.objects.filter(pk=self.instance.parent.pk)
            .only(field)
            .first()
        )
        if parent_instance:
            original_value = getattr(parent_instance, field, None)
            if original_value != value:
                return f"{field} cannot be modified. Original value: {original_value}."
        return None
