from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import *
from .helpers import *
from django.contrib.auth import authenticate , login


class LoginView(APIView):

    def post(self , request):
        responce ={}
        responce['status'] = 500
        responce['message'] = 'Something went wrong'
        try:
            data = request.data

            if data.get('username') is None:
                responce['message'] = 'key username not found'
                raise Exception('key username not found')
            
            if data.get('password') is None:
                responce['message'] = 'key password not found'
                raise Exception('key password not found')  


            check_user =User.objects.filter(username = data.get('username')).first()

            if check_user is None:
                responce['message'] = 'invalid username , user not found'
                raise Exception('invalid username not found')  

            if not Profile.objects.filter(user = check_user).first().is_verified:
                responce['message'] = 'your profile is not verified'
                raise Exception('profile not verified')  


            user_obj= authenticate(username = data.get('username'), password = data.get('password'))
            if user_obj:
                login(request, user_obj)
                responce['status'] = 200
                responce['message'] = 'Welcome'           
            else:
                responce['message'] = 'invalid password'
                raise Exception('invalid password')  
        except Exception as e :
            print(e)
        return Response(responce)




LoginView = LoginView.as_view()             

class RegisterView(APIView):

    def post(self , request):
        responce ={}
        responce['status'] = 500
        responce['message'] = 'Something went wrong'
        try:
            data = request.data

            if data.get('username') is None:
                responce['message'] = 'key username not found'
                raise Exception('key username not found')
            
            if data.get('password') is None:
                responce['message'] = 'key password not found'
                raise Exception('key password not found')  


            check_user =User.objects.filter(username = data.get('username')).first()

            if check_user:
                responce['message'] = 'username already taken, please use different username'
                raise Exception('username already taken, please use different username')  

            user_obj= User.objects.create(email = data.get('username'),username=data.get('username'))
            user_obj.set_password(data.get('password'))
            user_obj.save() 
            token = generate_random_string(20)
            Profile.objects.create(user = user_obj , token = token)
            print(user_obj)
            send_mail_to_user(token, data.get('username'))


            responce['message'] = 'Congratulations, you have successfully registered'
            responce['status']=200
        except Exception as e :
            print(e)
        return Response(responce)

RegisterView=RegisterView.as_view()