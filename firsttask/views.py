from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from data.chartdata import Data

from rest_framework.views import APIView
from rest_framework.response import Response

class HomeView(View):
    def get(self, request, *args, **kwargs):
        #getting transform values for each year from data
        return render(request, 'charts.html')


def get_data(request, *callback_args, **callback_kwargs):
    """Sends data as json response 
        I might change this to use django rest frameworks
    Returns:
        [Jsonresponse]: [We send our data as json response, in html we use ajax to get this.]
    """
    d = Data()
    data = d.get_data()
    tvals = d.get_transform_values()
    data['tvals'] = []
    data['tvals'].append(tvals)
    return JsonResponse(data)

class ChartData(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        """
        Rest framework way for sending data.
        """
        d = Data()
        data = d.get_data()
        tvals = d.get_transform_values()
        data['tvals'] = []
        data['tvals'].append(tvals)
        return Response(data)