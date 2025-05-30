import requests
from rest_framework.views import APIView
from rest_framework.response import Response


class NamozVaqtlariAPIView(APIView):
    def get(self, request):
        region = request.query_params.get('region', 'Toshkent')
        time_type = request.query_params.get('type', 'day')

        endpoints = {
            'day': 'present/day',
            'month': 'monthly',
            'year': 'yearly'
        }

        if time_type not in endpoints:
            return Response({"error": "Noto'g'ri 'type'. Faqat: day, month, year"}, status=400)

        url = f"https://islomapi.uz/api/{endpoints[time_type]}?region={region}"
        try:
            response = requests.get(url)
            if response.status_code != 200:
                return Response({"error": "API javob bermadi"}, status=response.status_code)

            data = response.json()

            # Agar bu kunlik bo‘lsa, times ichidagi nomlarni o‘zgartiramiz
            if time_type == 'day' and 'times' in data:
                original_times = data['times']
                renamed_times = {
                    'bomdod': original_times.get('tong_saharlik'),
                    'quyosh': original_times.get('quyosh'),
                    'peshin': original_times.get('peshin'),
                    'asr': original_times.get('asr'),
                    'shom': original_times.get('shom_iftor'),
                    'hufton': original_times.get('hufton'),
                }
                data['times'] = renamed_times

            return Response(data)

        except Exception as e:
            return Response({"error": str(e)}, status=500)
