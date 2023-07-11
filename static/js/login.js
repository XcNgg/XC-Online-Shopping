// 检测邮箱格式
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

// 登录验证接口
function checkLogin() {

    var formData = {
        email: $('input[name=email]').val(),
        password: $('input[name=password]').val(),
        captcha_code: $('input[name=captcha_code]').val()
    };
    // 发送登录请求
    $.ajax({
        url: '/users/CheckLogin', // 后端登录接口的URL
        type: 'POST',
        data: formData,
        dataType: 'json',
        success: function (response) {
            if (response.code === 200) {
                // 登录成功
                $("#error_alert").hide();
                $('#success-alert').show(); // 显示成功提示框
                setTimeout(function () {
                    window.location.href = '/'; // 登录成功后跳转到首页
                }, 500); // 0.5秒后跳转
            } else {
                // 登录失败
                $('#error_alert').text(response.message).show(); // 显示错误提示信息
                // 重置验证码
                GetCaptchaImage();
            }
        },
        error: function (xhr, status, error) {
            console.log(error); // 打印错误信息
        }
    });
}


// 重置验证码接口
function GetCaptchaImage() {
    $.ajax({
        url: '/users/ImageCaptcha',
        type: 'GET',
        success: function (response) {
            $('#captchaImage').attr('src', 'data:image/png;base64,' + response);
        },
        error: function (error) {
            console.log('Error:', error);
        }
    });
}


$(document).ready(function () {
    // 登录表单验证
    $('form').submit(function (event) {
        var password = $('input[name="password"]').val();
        var errors = [];
        if (!checkEmail()) {
            errors.push('邮箱格式不正确');
        }
        if (password.length < 8 || password.length > 20) {
            errors.push('密码长度须在8-20之间');
        }
        if (errors.length > 0) {
            var errorMessage = errors.join('<br>'); // Join error messages with <br> tags
            // Append error messages after the existing div element with id 'first_error'
            $("#error_alert").html(errorMessage).show();
            event.preventDefault(); // Prevent form submission
        } else {
            $("#error_alert").hide();
        }
    });

    // 点击登录，自动获取图像验证码
    GetCaptchaImage();

    // 点击重置
    $('#captchaImage').click(function () {
        GetCaptchaImage();
    });

    // 传参登录
    $('#LoginButton').click(function () {
        // 监听表单提交事件
        if ($('#RegistSuccess').length) {
          $('#RegistSuccess').hide();

        }
        checkLogin();
        // 获取表单数据
    });

});