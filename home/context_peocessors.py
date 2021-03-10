from .models import MVUser
def userinfo(request):
    if request.user.username!="":
        userinfo=MVUser.objects.get(DjangoUser=request.user)
    else:
        userinfo=None
    return {"userinfo":userinfo}