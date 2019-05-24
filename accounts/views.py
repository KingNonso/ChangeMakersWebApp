from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.shortcuts import redirect, render

from .forms import MembershipForm, UserRegistrationForm
from .models import Member
from .tasks import send_new_user_welcome_email_task


def register(request):
    member = MembershipForm(request.POST or None, request.FILES or None)
    user_form = UserRegistrationForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if user_form.is_valid() and member.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.is_active = True # should be false in final production
            # Save the User object
            new_user.save()
            # Create the user membership
            primary_phone = member.cleaned_data['primary_phone']
            membership_type = member.cleaned_data['membership_type']
            nse_no = member.cleaned_data['nse_no']
            dob = member.cleaned_data['dob']
            work = member.cleaned_data['work']
            job = member.cleaned_data['job']
            bio = member.cleaned_data['bio']
            photo = member.cleaned_data['photo']
            member = Member.objects.create(user=new_user, primary_phone=primary_phone, membership_type=membership_type, nse_no=nse_no, dob=dob, work=work, job=job, bio=bio, photo=photo)
            messages.success(request, 'Your registration was successful and your Membership Profile created successfully')
            host = 'HTTPS' if request.is_secure() else 'HTTP'
            host += '://'+str(request.get_host())
            print(host, )
            send_new_user_welcome_email_task.delay(new_user.email, member.id, host)
            return redirect('login')
        else:
            messages.add_message(request, messages.ERROR, 'Your last submission was not successful, please rectify and re-submit', extra_tags='danger')
    return render(request, 'accounts/register.html', {'form': member, 'user_form': user_form})


def activate_user_view(request, code=None, *args, **kwargs):
    pass
