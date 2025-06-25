from import_export import resources
from .models import Insurance_number

class InsuranceNumberResource(resources.ModelResource):
    class Meta:
        model = Insurance_number
        fields = [ 'notes' ,'Number', 'MassarCode', 'LastName', 'FirstName',]

class OffBudgetControlResource(resources.ModelResource):
    class Meta:
        model = Insurance_number
        fields = [ 'notes', 'Additional_fees', 'sport_ass', 'Insurance_fees', 'Number', 'MassarCode', 'LastName','FirstName']
