$(function () {
    bindCaptchaBtnClick();
});

function bindCaptchaBtnClick() {
    $('#email-captcha-btn').on('click', function (event) {
        var $this = $(this);
        var email = $('input[name="email"]').val();
        var successAlert = $('.alert-success.custom-alert');
        var dangerAlert = $('.alert.alert-danger');

        if (!email) {
            dangerAlert.show();
            successAlert.hide();
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
            url: "/users/email",
            method: "POST",
            data: {
                "email": email,
            },
            success: function (res) {
                var code = res['code'];
                if (code == 200) {
                    successAlert.show();
                    dangerAlert.hide();

                } else {
                    dangerAlert.show();
                    successAlert.hide();
                }
            }
        });
    });
}
