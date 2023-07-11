$(document).ready(function() {
  // 获取DOM元素和其他代码逻辑
  const editButton = $("#editButton");
  const commitButton = $("#commitButton");
  const cancelButton = $("#cancelButton");
  const editUsernameInput = $("#editUsername");
  // const editEmailInput = $("#editEmail");
  const usernameSpan = $("#username");
  const emailSpan = $("#email");

  // 点击编辑信息按钮的事件处理程序
  editButton.click(function() {
    // 显示编辑输入框并隐藏文本
    editUsernameInput.show();
    // editEmailInput.show();
    usernameSpan.hide();
    // emailSpan.hide();

    // 将对应的值传递给编辑输入框
    editUsernameInput.val(usernameSpan.text());
    // editEmailInput.val(emailSpan.text());

    // 切换按钮的显示状态
    editButton.hide();
    commitButton.show();
    cancelButton.show();
  });

  // 点击取消编辑按钮的事件处理程序
  cancelButton.click(function() {
    // 显示文本并隐藏编辑输入框
    usernameSpan.show();
    emailSpan.show();
    editUsernameInput.hide();
    // editEmailInput.hide();

    // 切换按钮的显示状态
    editButton.show();
    commitButton.hide();
    cancelButton.hide();
  });

  // 点击确认提交按钮的事件处理程序
  commitButton.click(function() {
    // 获取编辑输入框的值
    const newUsername = editUsernameInput.val();
    // const newEmail = editEmailInput.val();

    // 更新文本值
    usernameSpan.text(newUsername);
    // emailSpan.text(newEmail);

    // 显示文本并隐藏编辑输入框
    usernameSpan.show();
    emailSpan.show();
    editUsernameInput.hide();
    // editEmailInput.hide();

    // 切换按钮的显示状态
    editButton.show();
    commitButton.hide();
    cancelButton.hide();
  });
});
