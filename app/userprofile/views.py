from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import Profile


def userprofile(request, username):
    user = User.objects.filter(username=username)  # if user exist
    if user:
        user = user[0]
        profile = Profile.objects.get(user=user)
        bio = profile.bio
        user_img = profile.image
        data = {'user_obj': user,
                'bio': bio,
                'userImg': user_img,
                }
        return render(request, 'userprofile/userprofile.html', data)
    else:
        return HttpResponse('No Such User')


@login_required
def saveProfile(request):
    if request.method == "POST":
        profile = Profile.objects.get(user=request.user)
        img = request.FILES.get("image")
        bio = request.POST.get("captions", "")
        if img:
            profile.image = img
        if bio:
            profile.bio = bio
        profile.save()
        return HttpResponseRedirect(reverse("userprofile:userprofile", args=(request.user.username,)))
    else:
        return HttpResponseRedirect(reverse("userprofile:userprofile", args=(request.user.username,)))
