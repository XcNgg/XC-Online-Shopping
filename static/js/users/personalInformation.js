$(function () {
    bindCaptchaBtnClick();
});

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

function checkEmail(editEmail) {
    // 邮箱正则表达式
    var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    // 使用正则表达式验证邮箱
    if (emailRegex.test(editEmail)) {
        return true;
    } else {
        return false;
    }
}


function ButtonActive() {
    const editButton = $("#editButton");
    const commitButton = $("#commitButton");
    const cancelButton = $("#cancelButton");
    const editUsernameInput = $("#editUsername");
    const editEmailInput = $("#editEmail");
    const usernameSpan = $("#username");
    const emailSpan = $("#email");

    // 点击编辑信息按钮的事件处理程序
    editButton.click(function () {
        // 显示编辑输入框并隐藏文本
        editUsernameInput.show();
        editEmailInput.show();
        usernameSpan.hide();
        emailSpan.hide();

        // 将对应的值传递给编辑输入框
        editUsernameInput.val(usernameSpan.text());
        editEmailInput.val(emailSpan.text());

        // 切换按钮的显示状态
        editButton.hide();
        commitButton.show();
        cancelButton.show();

        $("#error_alert").hide();
        $('#success_alert').hide(); // 显示成功提示框
    });

    // 点击取消编辑按钮的事件处理程序
    cancelButton.click(function () {
        // 显示文本并隐藏编辑输入框
        usernameSpan.show();
        emailSpan.show();
        editUsernameInput.hide();
        editEmailInput.hide();

        // 切换按钮的显示状态
        editButton.show();
        commitButton.hide();
        cancelButton.hide();
        $("#error_alert").hide();
        $('#success_alert').hide(); // 显示成功提示框
    });

    // 点击确认提交按钮的事件处理程序
    commitButton.click(function () {
        // 获取编辑输入框的值
        checkEditInfo();
    });
}


function checkEditInfo() {
    const editButton = $("#editButton");
    const commitButton = $("#commitButton");
    const cancelButton = $("#cancelButton");
    const editUsernameInput = $("#editUsername");
    const editEmailInput = $("#editEmail");
    const usernameSpan = $("#username");
    const emailSpan = $("#email");

    const newUsername = editUsernameInput.val();
    const newEmail = editEmailInput.val();


    if (!checkUsername(editUsernameInput.val())) {
        $('#error_alert').text('用户名只能包含中文、大小写英文字母、下划线和数字').show();
        return false;
    }

    if (!checkEmail(editEmailInput.val())) {
        $('#error_alert').text('邮箱格式错误').show();
        return false;
    }

    console.log(usernameSpan);
    $.ajax({
        url: '/users/checkEditInfo',
        type: 'POST',
        data: {
            editUsername: editUsernameInput.val(),
            editEmail: editEmailInput.val(),
        },

        success: function (response) {
            if (response.code === 200) {
                $("#error_alert").hide();
                $('#success_alert').text('信息修改成功').show(); // 显示成功提示框

                // 显示文本并隐藏编辑输入框
                usernameSpan.show();
                emailSpan.show();
                editUsernameInput.hide();
                editEmailInput.hide();

                // 更新文本值
                usernameSpan.text(newUsername);
                emailSpan.text(newEmail);
                // 切换按钮的显示状态
                editButton.show();
                commitButton.hide();
                cancelButton.hide();
                return true;
            } else {
                $("#error_alert").text('信息修改失败,' + response.message).show();// 显示失败提示框
                $('#success_alert').hide();
                return false;
            }
        },
        error: function (error) {
            console.log('Error:', error);
            return false;
        }
    });
}


$(document).ready(function () {
    // 获取DOM元素和其他代码逻辑
    ButtonActive();

});
