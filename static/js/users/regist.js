$(function () {
    bindCaptchaBtnClick();
});


// 弹窗显示，如果值为1，绿色，如果值为2，则红色
function toggleDiv(divValue, divType) {
    if (divType === 2) {
        $('.alert.alert-danger').text(divValue).show();
        $('.alert.alert-success.custom-alert').hide();
    } else if (divType === 1) {
        $('.alert.alert-success.custom-alert').text(divValue).show();
        $('.alert.alert-danger').hide();
    }
}


// 用户名只包含中文、大小写英文字母、下划线和数字
function checkUsername(username) {
    // 使用正则表达式定义允许的字符规则
    var pattern = /^[\u4e00-\u9fa5a-zA-Z0-9_]+$/;
    // 检查用户名是否符合规则
    if (pattern.test(username)) {
        return true;  // 符合规则
    } else {
        return false;  // 不符合规则
    }
}


// 邮箱格式验证
function checkEmail() {
    // 邮箱正则表达式
    var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    var email = $('input[name="email"]').val();
    // 使用正则表达式验证邮箱
    if (emailRegex.test(email)) {
        return true;
    } else {
        return false;
    }
}

// 发送验证码前检查一遍是否全部填写了
function checkInputFields() {
    var username = $('input[name="username"]').val();
    var email = $('input[name="email"]').val();
    var password = $('input[name="password"]').val();
    var passwordConfirm = $('input[name="password_confirm"]').val();

    if (!username) {
        toggleDiv('用户名未输入，请检查!', 2);
        return false;
    }

    if (!checkUsername(username)) {
        toggleDiv('用户名只能包含中文、大小写英文字母、下划线和数字!', 2);
        return false;
    }

    if (username.length < 3 || username.length > 10) {
        toggleDiv('用户名长度须3-10字符', 2);
        return;
    }

    if (!email) {
        toggleDiv('邮箱未输入，请检查!', 2);
        return false;
    }

    if (!checkEmail()) {
        toggleDiv('邮箱格式不正确', 2);
        return;
    }

    if (password.length < 8 || password.length > 20) {
        toggleDiv('密码长度须在8-20之间', 2);
        return;
    }

    if (password !== passwordConfirm) {
        toggleDiv('密码不一致！请检查！', 2);
        return false;
    }

    return true;
}

// 邮箱验证码发送
function bindCaptchaBtnClick() {
    // 邮箱验证码验证
    $('#email-captcha-btn').on('click', function (event) {
        var $this = $(this);
        var successAlert = $('.alert-success.custom-alert');
        var dangerAlert = $('.alert.alert-danger');

        if (!checkInputFields()) {
            return;
        }

        $this.off('click');
        var countDown = 60;
        var timer = setInterval(function () {
            countDown -= 1;
            if (countDown > 0) {
                $this.text(countDown + "秒后可重新获取");
            } else {
                $this.text("获取验证码");
                bindCaptchaBtnClick();
                clearInterval(timer);
            }
        }, 1000);
        successAlert.hide();
        dangerAlert.hide();


        $.ajax({
            url: "/users/EmailCaptcha",
            method: "POST",
            data: {
                "email": $('input[name="email"]').val(),
                'username': $('input[name="username"]').val(),
                'timestamp': Math.floor(Date.now() / 1000)
            },
            success: function (res) {
                var code = res['code'];
                if (code === 200) {
                    toggleDiv('验证码发送成功', 1);
                } else {
                    toggleDiv('验证码发送失败,' + res['message'], 2);
                }
            }
        });
    });
}


$(document).ready(function () {

    $('#checkRegist').click(function (event) {
        var captcha = $('input[name="captcha"]').val();
        if (!checkInputFields()) {
            return;
        }

        if (!captcha) {
            toggleDiv('验证码为空', 2);
            return;
        } else if (captcha.length !== 6) {
            toggleDiv('验证码长度有误', 2);
            return;
        }

        $.ajax({
            url: "/users/CheckRegist",
            method: "POST",
            data: {
                "email": $('input[name="email"]').val(),
                'username': $('input[name="username"]').val(),
                'password': $('input[name="password"]').val(),
                'captcha': captcha,
            },
            success: function (res) {
                var code = res['code'];
                if (code === 200) {
                    toggleDiv('注册成功！即将跳转... ', 1);
                    setTimeout(function () {
                        window.location.href = '/users/login'; // 登录成功后跳转到首页
                    }, 500); // 0.5秒后跳转
                } else {
                    toggleDiv('注册失败,' + res['message'], 2);
                }
            }
        });
    });

    $(document).keypress(function (event) {
        if (event.which === 13) {  // 检测按下的键是否是回车键
            $('#checkRegist').click();  // 触发按钮的点击事件
        }
    });

});


