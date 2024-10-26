from django.shortcuts import render
from django.shortcuts import render,HttpResponse,redirect


from django.views.generic  import View

from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages

# to activate the user accounts
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import NoReverseMatch,reverse
from django.template.loader import render_to_string
# from  django.utils.encoding import force_bytes,force_text,DjangoUnicodeDecodeError
# getting tokens from utilis.py
from .utilis import TokenGenerator
from .utilis import generate_tokens
from django.utils.encoding import force_str



#emails
from django.core.mail import send_mail,EmailMultiAlternatives
from django.core.mail import BadHeaderError,send_mail
from django.core import mail
from django.conf import settings
from django.core.mail import EmailMessage
from threading import Thread

#reset password generator
from django.contrib.auth.tokens import PasswordResetTokenGenerator






#threading\
import threading
from django.core.mail import EmailMessage
from django.core.cache import cache
cache.clear()




class EmailThread(threading.Thread):
    def __init__(self, email_message):
        if not isinstance(email_message, EmailMessage):
            raise ValueError("email_message must be an instance of EmailMessage")
        self.email_message = email_message
        super().__init__()

    def run(self):
        self.email_message.send()

# Example of creating and sending an email
email = EmailMessage(
    'Subject here',
    'Here is the message.',
    'from@example.com',
    ['to@example.com']
)

# Start the email thread
EmailThread(email).start()



def signup(request):
    if request.method=='POST':
         email=request.POST.get('email')
         pass1=request.POST.get('pass1')
         pass2=request.POST.get('pass2')
         if pass1 != pass2:

        
        
          messages.warning(request,"password is not matching")
        
        
          return render(request,'auth/signup.html')

         try:
            
            if User.objects.get(username=email):
                messages.warning(request,"email is Taken")
                return render(request,'auth/signup.html')
         except Exception as identifier:
            
           pass
         user=User.objects.create_user(email,email,pass1)
         user.is_active=False
         
         user.save()
         current_site=get_current_site(request)
         email_subject="Activate Your Account"
         message=render_to_string('auth/activate.html',{'user':user,'domain':'127.0.0.1:8000',
                                             'uid' :urlsafe_base64_encode(force_bytes(user.pk)) ,
                                               'token'  :  generate_tokens.make_token(user),      
                                                           })
         
         email_message=EmailMessage(email_subject,message,settings.EMAIL_HOST_USER,[email],)
         
         EmailThread(email_message).start()
         messages.info(request,"Activate Your Account by clicking link on your email")
        
         return render(request,'auth/login.html')
    return render(request,'auth/signup.html')
    
       
       
       
       
    
       
class ActivateAccountView(View):
       def  get(self,request,uidb64,token):
        try:
           uid=force_str(urlsafe_base64_decode(uidb64))
           user=User.objects.get(pk=uid)
        except Exception as identifier:
           
              user=None
        if user is not None and generate_tokens.check_token(user,token):
              user.is_active=True
              user.save()
              messages.info(request,"Account Activated succesfully")
              return redirect ('/arkauth/login')
        return render(request,'auth/activatefail.html')
def handlelogin(request):
    
    if request.method=='POST':
         
         password1=request.POST.get('password1')
         
         email=request.POST.get('email')
         myuser=authenticate(username=email,password=password1)
        
         if myuser is not None:
            login(request,myuser)
            messages.success(request,'login Success')
            return render(request,'index.html')
        
         else:
            messages.error(request,"something went wrong")
            
            return redirect ('/arkauth/login')
    
    
    
    return render(request,'auth/login.html')


def handlelogout(request):
    logout(request)
    messages.success(request,"logout Success")
    return redirect('/arkauth/login')





class RequestResetEmailView(View):
    def get (self,request):
        
      return render(request,'auth/request-reset-email.html')

    def post(self,request):
        email=request.POST['email']
        user=User.objects.filter(email=email)
        
        
        
        if user.exists():
           current_site= get_current_site(request)
           email_subject='[Reset your password]'
           message=render_to_string('auth/reset-user-password.html',
           {
               
               'domain':'127.0.0.1:8000',
                'uid':urlsafe_base64_encode(force_bytes(user[0].pk)),
                'token':PasswordResetTokenGenerator().make_token(user[0])
           })

        email_message=EmailMessage(email_subject,messages,settings.EMAIL_HOST_USER,[email])

        
        EmailThread(email_message).start()
        messages.info(request,"We Have sent you a email with instructions on how to reset a password ")

        return render(request,'auth/request-reset-email.html')




class SetNewPasswordView(View):
    def get(self,request,uidb64,token):
        context={
            'uidb64':uidb64,
            'token':token
        }
        
        try:
            user_id=force_text(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=user_id)
            
            if not PasswordResetTokenGenerator().check_token(user,token):
                messages.warning(request,'password reset link is invalid')
                
                
                return render(request,'auth/request-reset-email.html')
            
        except DjangounicodeDecodeError as identifier:
            pass
        
        return render(request,'auth/set-new-password.html',context)
        
        
        
        def post(self,request,uidb64,token):
            context={
                'uidb64':uidb64 ,
                'token':token
                }                    
            pass1=request.POST.get('pass1')
            pass2=request.POST.get('pass2')
            if pass1 != pass2:

        
        
              messages.warning(request,"password is not matching")
        
        
              return render(request,'auth/set_new-password.html',context)
          
          
            try:
                user_id=force_text(urlsafe_base64_decode(uidb64))
                usdr=User.objects.get(pk=user_id)
                user.set_password()
                user.save()
                messages.success(requewst,"password Reset success please login with a new password ")
                
                
                return redirect('/arkauth/login')
          
          
          
            except DjangounicodeDecodeError as  identifier:
                messages.error(request,'something went wrong')
                return redirect(request,'auth/set-new-password.html',context)
            return render(request,'auth/set-new-password.html',context)
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          

         
            
            