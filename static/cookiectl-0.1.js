(function (jq){
    function setCookie(c_name, value, expiredays) {
        var exdate = new Date();
        exdate.setDate(exdate.getDate() + expiredays);
        c_start = document.cookie.indexOf(c_name + "=");
        document.cookie = c_name + "=" + decodeURI(value) +
            ((expiredays == null) ? "" : ";expires=" + exdate.toGMTString())
    }

    function getCookie(c_name) {
        if (document.cookie.length > 0) {
            c_start = document.cookie.indexOf(c_name + "=");
            if (c_start != -1) {
                c_start = c_start + c_name.length + 1;
                c_end = document.cookie.indexOf(";", c_start);
                if (c_end == -1) c_end = document.cookie.length;
                return decodeURIComponent(document.cookie.substring(c_start, c_end))
            }
        }
        return ""
    }


    jq.extend({
        checkLoginStatus: function (csrftoken) {
            var LoginStatus = getCookie('login_status');
            var UserName = getCookie("username");
            var PassWord = getCookie("password");
            var CsrfToken = csrftoken;
            console.log('username:', UserName, 'password:', PassWord, "login_status:", LoginStatus);
            if (LoginStatus && UserName != "" && UserName != null) {
                $.post('/sign.html/', {
                    'username': UserName, 'password': PassWord, 'csrfmiddlewaretoken': CsrfToken
                }, function () {
                    window.location.href = '/index.html/'
                });
            }
            else {
                setCookie(UserName, '', -1);
                setCookie(PassWord, '', -1);
            }
        }
    })
})(jQuery);