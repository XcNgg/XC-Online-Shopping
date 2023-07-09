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