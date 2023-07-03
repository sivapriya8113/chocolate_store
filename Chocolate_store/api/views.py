from django.contrib.auth import login
from django.shortcuts import redirect, render
from rest_framework import generics, permissions, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response

from .models import Chocolate
from .serializers import ChocoSerializer, RegisterSerializer, LoginSerializer


class RegisterView(generics.CreateAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'signup.html'
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # token, created = Token.objects.get_or_create(user=user)
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request,user)
        # token, created = Token.objects.get_or_create(user=user)
        return Response(status=status.HTTP_201_CREATED)


class ListChocolate(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'list.html'
    queryset = Chocolate.objects.all()
    serializer_class = ChocoSerializer

    def list(self, request):
        queryset = self.get_queryset()
        # serializer = ChocoSerializer(queryset, many=True)
        return Response({'object_list': queryset})


class DetailChoco(RetrieveUpdateDestroyAPIView):
    # authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'detail.html'
    queryset = Chocolate.objects.all()
    serializer_class = ChocoSerializer

    def get(self, request, *args, **kwargs):
        # Your custom GET method logic here
        queryset = self.get_object()
        if queryset is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        authenticated = request.user.is_authenticated
        print('######', authenticated)
        if not authenticated:
            return redirect('list')
        return Response({'object': queryset, 'authenticated': authenticated})


class ChocoCheckoutView(RetrieveUpdateDestroyAPIView):  # LoginRequiredMixin
    permission_classes = [AllowAny]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'checkout.html'
    queryset = Chocolate.objects.all()
    serializer_class = ChocoSerializer

    def get(self, request, *args, **kwargs):
        queryset = self.get_object()
        if queryset is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        authenticated = request.user.is_authenticated
        print('######', authenticated)
        if not authenticated:
            return redirect('list')
        return Response({'object': queryset, 'authenticated': authenticated})

# class CartView(ViewSet):
#     # authentication_classes = [authentication.TokenAuthentication]
#     # permission_classes = [permissions.IsAuthenticated]
#
#     def list(self, request, *args, **kwargs):
#         qs = Carts.objects.all()
#         serializer = CartSerializer(qs, many=True)
#         return Response(data=serializer.data)
#
# def destroy(self, request, *args, **kwargs):
#     id = kwargs.get('pk')
#     object = Carts.objects.get(id=id)
#     if object.user == request.user:
#         object.delete()
#         return Response(data="deleted")
#     else:
#         raise serializers.ValidationError("You have no permission to perform this operation")

#     @action(methods=['GET'], detail=True)
#     def add_quantity(self, request, *args, **kwargs):
#         id = kwargs.get('pk')
#         try:
#             qs = Carts.objects.get(id=id)
#             qs.quantity += 1
#             qs.save()
#         except:
#             return Response('There is no such item')
#         return Response('updated')
#
#     @action(methods=["GET"], detail=True)
#     def minus_quantity(self, request, *args, **kwargs):
#         id = kwargs.get('pk')
#         try:
#             qs = Carts.objects.get(id=id)
#             qs.quantity -= 1
#             qs.save()
#         except:
#             return Response('There is no such file')
#         return Response('updated')
def home(request):
    return render(request,'home.html')