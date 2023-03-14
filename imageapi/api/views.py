from django.http import FileResponse, HttpResponse
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from core.models import Images
from rest_framework import status, generics
from .serializers import ListImageSerializer, SmallImageSerialzier, MediumImageSerialzier, OriginalImageSerialzier, \
    CustomImageSerialzier, ImagaViewSerializer
from .permissions import NormalPermission, EnterprisePermission, PremiumPermission, RootPermission, IsUploader


class UploadSmallImage(APIView):
    serializer_class = SmallImageSerialzier
    permission_classes = [IsAuthenticated, NormalPermission]

    def get_serializer_context(self):
        return {'request': self.request}

    def post(self, request, *arg, **kwargs):
        serializer = self.serializer_class(data=request.data, context=self.get_serializer_context())
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "Uploaded"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UploadMediumImage(APIView):
    permission_classes = [IsAuthenticated, PremiumPermission]

    def get_serializer_context(self):
        return {'request': self.request}

    def post(self, request, *arg, **kwargs):
        serializer = MediumImageSerialzier(data=request.data, context=self.get_serializer_context())
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "Uploaded"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UploadOriginalImage(APIView):
    permission_classes = [IsAuthenticated, PremiumPermission]

    def get_serializer_context(self):
        return {'request': self.request}

    def post(self, request, *arg, **kwargs):
        serializer = OriginalImageSerialzier(data=request.data, context=self.get_serializer_context())
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "Uploaded"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UploadCustomImage(APIView):
    serializer_class = CustomImageSerialzier
    permission_classes = [IsAuthenticated, RootPermission]

    def get_serializer_context(self):
        return {'request': self.request}

    def post(self, request, *arg, **kwargs):
        serializer = self.serializer_class(data=request.data, context=self.get_serializer_context())
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "Uploaded"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListImage(generics.ListAPIView):
    serializer_class = ListImageSerializer
    permission_classes = [IsAuthenticated, NormalPermission]

    def get_queryset(self):
        query = Images.objects.filter(uploaded_by=self.request.user)
        return query


class ImageView(generics.RetrieveAPIView):
    serializer_class = ImagaViewSerializer
    lookup_field = 'id'

    def get_queryset(self):
        return Images.objects.filter(id=self.kwargs['id'])

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance.is_expired():
            with open(instance.image.path, 'rb') as f:
                response = HttpResponse(f.read(), content_type='image/png')
                response['Content-Disposition'] = 'inline; filename=image.png'
                return response
        return Response({"error": {"Sorry, the link is expired"}}, status=status.HTTP_403_FORBIDDEN)
