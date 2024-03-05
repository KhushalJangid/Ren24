from account.functions import getPass

# Create context processor so our pass can work on all pages of the site
def _pass(request):
    if request.user.is_authenticated:
        return {'pass': getPass(request.user)}
    else:
        return {'pass':None}