from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.

@login_required(login_url='login')
def profile(request):
    user = request.user
    return render(request, 'profile.html', {
        'user': user,
        'bookdues': user.bookdues,
        'wishlist': user.wishlist.all(),
    })

@login_required(login_url='login')
def profile_edit(request):
    user = request.user
    if request.method == 'POST':
        userdob = request.POST.get('userdob')
        profile_pic = request.FILES.get('profile_pic')
        if userdob:
            user.userdob = userdob
        if profile_pic:
            user.profile_pic = profile_pic
        user.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')
    return render(request, 'profile_edit.html', {'user': user})
