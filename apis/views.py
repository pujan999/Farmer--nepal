from django.shortcuts import render
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from .seriallizer import ProductSerializers, VendorSerializers
from market.models import Product, Vendor
from rest_framework import status



@api_view(["GET"])
def ProductApi(request):
    product_details = Product.objects.all()
    serializer = ProductSerializers(product_details, many=True)

    return Response(serializer.data)



@api_view(["GET", "POST", "PUT", "PATCH", "DELETE"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def Vendor_details(request, pk=None):
    if request.method == "GET":
        id = pk
        if id is not None:
            Vendor_details = Vendor.objects.get(id=id)
            serializer = VendorSerializers(Vendor_details)
            return Response(serializer.data)
        else:
            Vendor_details = Vendor.objects.all()
            serializer = VendorSerializers(Vendor_details, many=True)
            return Response(serializer.data)

    if request.method == "POST":
        serializer = VendorSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            res = {"msg": "Vendor is Created"}
            return Response(res, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    if request.method == "PUT":
        id = pk
        Vendor_details = Vendor.objects.get(id=id)
        serializer = VendorSerializers(Vendor_details,
                                       data=request.data,
                                       partial=True)
        if serializer.is_valid():
            serializer.save()
            res = {"msg": "Vendor is Updated"}
            return Response(res, status=status.HTTP_206_PARTIAL_CONTENT)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    if request.method == "PATCH":
        id = pk
        Vendor_details = Vendor.objects.get(id=id)
        serializer = VendorSerializers(Vendor_details, data=request.data)
        if serializer.is_valid():
            serializer.save()
            res = {"msg": "Vendor is Updated"}
            return Response(res, status=status.HTTP_206_PARTIAL_CONTENT)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    if request.method == "DELETE":
        id = pk
        Vendor_details = Vendor.objects.get(id=id)
        Vendor_details.delete()
        return Response(serializer.data, status=status.HTTP_410_GONE)



@api_view(['POST'])
def vendorregistiation(request):
    print(request.data)
    return Response(serializer.data,status=status.HTTP_200_OK)