from django.contrib.auth import authenticate, login
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.forms import LoginForm

from .models import Member
from .serializers import MemberSerializer


class Login(APIView):

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            username=cd['username']
            user = authenticate(request,
                                username=username,
                                password=cd['password'])
            if user is not None:
                if user.is_active and Member.objects.filter(user__username=username):
                    login(request, user)
                    serializer_context = {
                        'request': request,
                    }
                    member = Member.objects.filter(user__username=username)[0]
                    serializer = MemberSerializer(member, context=serializer_context)
                    return Response(serializer.data)
                else:
                    return Response({'status': 'inactive'})

        return Response({'status': 'ko'})
