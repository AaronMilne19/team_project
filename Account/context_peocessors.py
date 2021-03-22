from home.models import MVUser
def userinfo(request):
    if request.user.username!="" and request.user.is_superuser!=True :
        userinfo=MVUser.objects.get(DjangoUser=request.user)

    else:
        userinfo=None
    return {"userinfo":userinfo}