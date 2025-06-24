from import_export import resources
from .models import Insurance_number

class InsuranceNumberResource(resources.ModelResource):
    class Meta:
        model = Insurance_number
        fields = ['Number', 'FirstName', 'LastName', 'MassarCode']

class OffBudgetControlResource(resources.ModelResource):
    class Meta:
        model = Insurance_number
        fields = ['Number', 'FirstName', 'LastName', 'MassarCode', 'Insurance_fees', 'sport_ass', 'Additional_fees']
