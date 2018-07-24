from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import RegistrationForm,EditProfile
from accounts.forms import EditProfile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm,PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from django.views.generic import UpdateView,View
from .models import UserAccount
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin


def home(request):
    return render(request,'accounts/home.html')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('home:home'))

    else:
        form = RegistrationForm()

        return render(request,'accounts/reg_form.html',{'form': form,})


def view_profile(request, pk=None):
    if pk:
        user = User.objects.get(pk=pk)
    else:
        user = request.user
    is_following=False
    if user.useraccount in request.user.is_following.all():
        is_following=True
    args = {'user': user,'is_following':is_following}
    return render(request, 'accounts/profile.html', args)

class UseraccountUpdate(UpdateView):
    model = UserAccount
    fields = ['discription','contact_no','city','website','image']
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('accounts:view_profile')

def edit_profile(request):
    if request.method=='POST':
        form=EditProfile(request.POST,instance=request.user)
        if form.is_valid():
            form.save()
            return redirect(reverse('accounts:view_profile'))

    else:
       form=EditProfile(instance=request.user)
       args={'form':form}
       return render(request,'accounts/edit_profile.html',args)


def edit_new_profile(request):
    if request.method == 'POST':
        form = EditProfile(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect(reverse('accounts:view_profile'))
    else:
        form = EditProfile(instance=request.user)
        args = {'form': form}
        return render(request, 'accounts/edit_profile.html', args)





def change_password(request):
    if request.method=='POST':
        form= PasswordChangeForm(data=request.POST,user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)

            return redirect(reverse('accounts:view_profile'))
        else:
            return redirect(reverse('accounts:change_password'))

    else:
        form=PasswordChangeForm(user=request.user)
        args={'form':form}
        return render(request,'accounts/edit_profile.html',args)



class ProfileFollowToggle(LoginRequiredMixin,View):

    def post(self,request,*args,**kwargs):

        user_to_toggle=request.POST.get('username')
        print(user_to_toggle)
        user_=User.objects.get(username__iexact=user_to_toggle)

        profile=UserAccount.objects.get(user__username__iexact=user_to_toggle)

        user=request.user

        if user in profile.follower.all():

            profile.follower.remove(user)
        else:

            profile.follower.add(user)

        return redirect(reverse('accounts:view_profile_with_pk',args=[user_.id]))







