import math

from django.db.models import Q, Sum, FloatField
from django.db.models.functions import Coalesce

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Amount


def truncate(number, digits) -> float:
    stepper = 10.0 ** digits
    return math.trunc(stepper * number) / stepper

class ClientAmountView(APIView):
    def get(self, request):
        id = request.GET.get('id', None)
        start_date = request.GET.get('start-date')
        end_date = request.GET.get('end-date', start_date)

        q = Q()

        if id is None:
            return Response({"message : client id는 필수값입니다."}, status=status.HTTP_400_BAD_REQUEST)

        if start_date is None and end_date is not None:
            return Response({"message : start-date를 설정하세요."}, status=status.HTTP_400_BAD_REQUEST)

        if id:
            q &= Q(advertiser = id)
        if start_date:
            q &= Q(date__range=[f"{start_date}", f"{end_date}"])

        amount = (Amount.objects
        .filter(q)
        .values('media')
        .annotate(
            CTR = Coalesce(Sum('click') * 100 / Sum('impression'),0,output_field=FloatField()),
            ROAS = Coalesce(Sum('cv') * 100 / Sum('cost'),0,output_field=FloatField()),
            CPC = Coalesce(Sum('cost') / Sum('click'),0,output_field=FloatField()),
            CVR = Coalesce(Sum('conversion') * 100 / Sum('click'),0,output_field=FloatField()),
            CPA = Coalesce(Sum('cost') / Sum('conversion'),0,output_field=FloatField())
            )
        )
        result = {}
        for i in amount:
            result[i['media']] = {
                'ctr' : truncate(i['CTR'], 2),
                'cpc' : truncate(i['CPC'], 2),
                'roas' : truncate(i['ROAS'], 2),
                'cvr' : truncate(i['CVR'], 2),
                'cpa' : truncate(i['CPA'], 2)
            }
        return Response(result, status=status.HTTP_200_OK)
