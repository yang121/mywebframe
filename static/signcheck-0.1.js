$('#passwordConfirm, #inputPassWord').focusout(
    function () {
        var PassWord = $('#inputPassWord').val();
        var PassWord2 = $('#passwordConfirm').val();
        if (PassWord && PassWord2 && PassWord2 != PassWord){
            $(this).siblings('span').text('两次密码不一致');
        }
        else {
            $(this).siblings('span').text('');
        }
    }
);

function isEmail(str) {
    var reg = new RegExp("^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+(.[a-zA-Z0-9_-])+");
    console.log('email:', reg.test(str.trim()));
    return reg.test(str.trim())
}

function isTel(str) {
    var reg = new RegExp("^1[0-9]{10}");
    console.log('tel:',reg.test(str.trim()));
    return reg.test(str.trim())
}


function formCommit(csrf_token) {

    var formData = new FormData();
    formData.append('csrfmiddlewaretoken', csrf_token);
    $('#sign-box input').each(function (k, v) {
        console.log('input:', k, v);
        if (v){

            var name = $(v).prop('name');
            var value = $(v).prop('value');
            formData.append(name, value);
        }
    });

    $.ajax({
            url: '/sign/sign-up.html?md=post',
            type: 'POST',
            data: formData,
            contentType: false,		// 告知jQuery不用处理数据(设置请求头)
            processData: false,		// 告知jQuery不用处理数据(设置请求头)
            dataType: "JSON",
            success: function(arg){
                console.log('arg.status', arg.status);
                if (arg.status){
                    self.location.href = '/index.html';
                }
                else {
                    // console.log(arg.errors);
                    $.each(arg.errors, function (k, v) {
                        console.log('kv:', k, v[0]);
                        if (k=='__all__'){
                            k = 'code';
                        }
                        $('input[name="'+ k + '"]').next('span').text(v[0]);
                    })
                }
            }
    })
}

(function (jq) {

    jq.extend({
        loginCheck: function (csrf_token) {
            $('#sign-btn, #reg-btn').click(function () {
                var flag = true;
                $('input').siblings('span').text('');
                $('input').each(function (k, v) {
                    if ($(v).val()){
                        $(v).siblings('span').text('');
                        if ($(v).prop('name') == ('username')) {
                            if ($(v).val().length < 6) {
                                $(v).siblings('span').text('用户名长度必须大于6');
                                flag = false;
                                return false
                            }
                            else if ($(v).val().length > 32) {
                                $(v).siblings('span').text('用户名长度必须小于32');
                                flag = false;
                                return false
                            }
                            else {
                                $(v).siblings('span').text('');
                            }
                        }

                        if ($(v).prop('name') == ('telephone')) {
                            if (!isTel($(v).val())) {
                                $(v).siblings('span').text('请输入正确的手机号码');
                                flag = false;
                                return false
                            }
                            else {
                                $(v).siblings('span').text('');
                            }
                        }

                        if ($(v).prop('name') == ('nickname')) {
                            if ($(v).val().length > 32) {
                                $(v).siblings('span').text('昵称长度必须小于32');
                                flag = false;
                                return false
                            }
                            else {
                                $(v).siblings('span').text('');
                            }
                        }

                        if ($(v).prop('name') == ('email')) {
                            if (!isEmail($(v).val())) {
                                $(v).siblings('span').text('请输入正确的邮箱地址');
                                flag = false;
                                return false
                            }
                            else {
                                $(v).siblings('span').text('');
                            }
                        }

                        if ($(v).prop('type') == ('password')) {
                            console.log($(v));
                            if ($(v).val().length < 6) {
                                $(v).siblings('span').text('密码长度必须大于6');
                                flag = false;
                                console.log('走这里:');
                                return false
                            }
                            else if ($(v).val().length > 64) {
                                $(v).siblings('span').text('密码长度必须小于64');

                                flag = false;
                                return false
                            }
                            else {
                                $(v).siblings('span').text('');
                            }
                        }

                    }
                    else {
                        if ($(v).attr('null')) {
                        }
                        else {
                            $(v).siblings('span').text($(this).prop('placeholder'));
                            flag = false;
                            return false
                        }
                    }



                });
                var PassWord = $('#inputPassWord').val();
                var PassWord2 = $('#passwordConfirm').val();

                if (PassWord && PassWord2 && PassWord != PassWord2){
                    flag = false;
                    $('#passwordConfirm').siblings('span').text('两次密码不一致');
                    return flag
                }

                if (flag){
                    formCommit(csrf_token);
                }
            })
        }
    });
})(jQuery);