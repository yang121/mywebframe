from django.conf import settings

class SessionManage:
    def __init__(self, request):
        self.request = request

    def sign_in(self, user):
        self.request.session['login_status'] = True
        self.request.session['username'] = user['username']
        self.request.session['uid'] = user['id']
        self.request.session['site'] = user['blog__site']
        if user['avatar']:
            self.request.session['avatar'] = user['avatar'].url
        else:
            self.request.session['avatar'] = settings.DEFAULT_IMG_PATH
        from rbac.service import initial_permission
        initial_permission(self.request, user['id'])
        print(self.request.session[settings.RBAC_PERMISSION_SESSION_KEY])
        if self.request.session[settings.RBAC_PERMISSION_SESSION_KEY].get('/backend.html'):
            self.request.session['backend'] = True

    def sign_out(self):
        self.request.session['login_status'] = False
        del self.request.session['username']
        del self.request.session['uid']
        del self.request.session['avatar']
        del self.request.session['site']
        del self.request.session[settings.RBAC_MENU_PERMISSION_SESSION_KEY]
        del self.request.session[settings.RBAC_PERMISSION_SESSION_KEY]
