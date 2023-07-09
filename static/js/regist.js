$(function () {
    bindCaptchaBtnClick();
});



// 弹窗显示，如果值为1，绿色，如果值为2，则红色
function toggleDiv(divValue, divType) {
      if (divType === 2) {
        $('.alert.alert-danger').text(divValue).show();
        $('.alert.alert-success.custom-alert').hide();
      }else if(divType === 1){
           $('.alert.alert-success.custom-alert').text(divValue).show();
        $('.alert.alert-danger').hide();
      }
}


// 邮箱格式验证
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

  if (!email) {
    toggleDiv('邮箱未输入，请检查!', 2);
    return false;
  }

  if (!password) {
    toggleDiv('密码未输入，请检查!', 2);
    return false;
  }

  if (!passwordConfirm) {
    toggleDiv('确认密码未输入，请检查!', 2);
    return false;
  }

  if (!checkEmail()) {
        toggleDiv('邮箱格式不规范,请检查！',2);
        return false;
  }

  if (password !== passwordConfirm) {
     toggleDiv('密码不一致！请检查！',2);
      return false;
  }

  return true;
}


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
                "email": email,
            },
            success: function (res) {
                var code = res['code'];
                if (code == 200) {
                    toggleDiv('验证码发送成功！请打开邮箱查收！',1);
                } else {
                     toggleDiv('验证码发送失败！请检查是否有效邮箱！',2);
                }
            }
        });
    });
}


$(document).ready(function() {
  $('form').submit(function(event) {
    var username = $('input[name="username"]').val();
    var password = $('input[name="password"]').val();
    var passwordConfirm = $('input[name="password_confirm"]').val();
    var captcha = $('input[name="captcha"]').val();

    var errors = [];
    if (username.length < 3 || username.length > 10) {
      errors.push('用户名长度须3-10字符');
    }
    if (!checkEmail()) {
      errors.push('邮箱格式不正确');
    }
    if (password.length < 8 || password.length > 20) {
      errors.push('密码长度须在8-20之间');
    }
    if (password !== passwordConfirm) {
      errors.push('两次密码不一致!');
    }
    if (!captcha){
        errors.push('验证码未输入！请检查！');
    }else if (captcha.length !== 6) {
        errors.push('验证码输入有误！请检查！');
    }



    if (errors.length > 0) {
       var errorMessage = errors.join('<br>'); // Join error messages with <br> tags
      // Append error messages after the existing div element with id 'first_error'
        $('.alert.alert-danger').html(errorMessage).show();
        event.preventDefault(); // Prevent form submission
    }else{
        $('.alert.alert-danger').hide();
    }
  });
});


