# views.py
import os
import csv
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Organization
from .serializers import AnnualDataSerializer

class AnnualDataView(APIView):
    def get_csv_file_path(self):
        # Get the path to the CSV file dynamically
        current_dir = os.path.dirname(os.path.abspath(__file__))
        csv_file_path = os.path.join(current_dir, 'inerg_data.csv')
        return csv_file_path

    def get(self, request):
        well_number = request.query_params.get('well')
        if not well_number:
            return Response({'error': 'Well number not provided'}, status=400)

        try:
            organization = Organization.objects.get(api_well_number=well_number)
            serializer = AnnualDataSerializer(organization)
            return Response(serializer.data)
        except Organization.DoesNotExist:
            return Response({'error': 'Organization not found'}, status=404)

    def post(self, request):
        try:
            csv_file_path = self.get_csv_file_path()
            response = self.load_annual_data_from_csv(csv_file_path)
            return response
        except Exception as e:
            return Response({'error': str(e)}, status=500)

    def load_annual_data_from_csv(self, csv_file):
        try:
            with open(csv_file, 'r') as file:
                reader = csv.DictReader(file)
                annual_data = {}
                for row in reader:
                    api_well_number = row.get('API WELL  NUMBER', '')
                    if not api_well_number:
                        continue
                    oil = int(row.get('OIL', '0').replace(',', ''))
                    gas = int(row.get('GAS', '0').replace(',', ''))
                    brine = int(row.get('BRINE', '0').replace(',', ''))

                    if api_well_number in annual_data:
                        annual_data[api_well_number]['oil'] += oil
                        annual_data[api_well_number]['gas'] += gas
                        annual_data[api_well_number]['brine'] += brine
                    else:
                        annual_data[api_well_number] = {'oil': oil, 'gas': gas, 'brine': brine}

                # Inserting data into the database
                for api_well_number, production in annual_data.items():
                    oil = production['oil']
                    gas = production['gas']
                    brine = production['brine']
                    Organization.objects.update_or_create(
                        api_well_number=api_well_number,
                        defaults={'oil': oil, 'gas': gas, 'brine': brine}
                    )

                print("Data successfully inserted into database.")

                # Return a success response
                return Response({'message': 'Data insertion successful'}, status=200)
        except Exception as e:
            # Return an error response
            return Response({'error': str(e)}, status=500)
