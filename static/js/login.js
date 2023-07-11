function checkEmail() {
  // 邮箱正则表达式
  var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  var email = $('input[name="email"]').val();
  // 使用正则表达式验证邮箱
    if ( emailRegex.test(email)){
        return true;
    }else {
        return false;
    }
}


// 登录表单验证
$(document).ready(function() {
  $('form').submit(function(event) {
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
    }else{
        $("#error_alert").hide();
    }
  });
});


// 重置验证码
function GetCaptchaImage() {
    $.ajax({
        url: '/users/ImageCaptcha',
        type: 'GET',
        success: function(response) {
            $('#captchaImage').attr('src', 'data:image/png;base64,' + response);
        },
        error: function(error) {
            console.log('Error:', error);
        }
    });
}

$(document).ready(function() {
    // Execute GetCaptchaImage() on initial website request
    GetCaptchaImage();
    $('#captchaImage').click(function() {
        GetCaptchaImage();
    });
});
