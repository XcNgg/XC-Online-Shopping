// productsinfo.js

$(document).ready(function () {
    var error_alert = $('#error_alert');
    var success_alert = $('#success_alert');
    var success_message = $('#success-message');


    // 添加点击事件监听器到 "确认下单" 按钮
  $("#sumbit-order").on("click", function () {
      error_alert.hide();
    success_alert.hide();
    // 获取购买数量输入框的值
    const buyNumber = $("#buy-number").val();
    if(buyNumber<0){
        error_alert.text('购买数量必须大于0');
        return false;
    }



    success_alert.show();
    success_message.text('确认订单中...').show();

    // 准备要发送的数据，以便在POST请求中使用
    var formData = new FormData();
    formData.append('productid',$('#product-id').text());
    formData.append('buyNumber',buyNumber);

    // 发起POST请求
    $.ajax({
      type: "POST",
      url: "/products/AddOrders",
      data: formData,
        processData: false,
        contentType: false,
      success: function (response) {
          if(response.code === 200){
            // 在成功完成订单检查后处理来自服务器的响应
            // 在此处添加代码以显示成功消息
            error_alert.hide();
            success_alert.show();
            success_message.text(response.message);
            setTimeout(function () {
                window.location.replace(`/users/BuyOrderInfo?id=${response.order_id}`);
            }, 1000); // 0.8秒后跳转

          }else if (response.code===302){
                    success_alert.hide();
               error_alert.text('请先登录！').show(); // 显示成功提示框
                setTimeout(function () {
                    window.location.href = '/users/login'; // 登录成功后跳转到首页
                }, 800); // 0.5秒后跳转
          }else{
            success_alert.hide();
               error_alert.text(response.message).show(); // 显示成功提示框
          }
      },
      error: function (error) {
        // 处理POST请求期间出现的任何错误
        console.log(error);
        error_alert.text('订单繁忙,请稍后重试').show();
        success_alert.hide();
      },
    });
  });
});
