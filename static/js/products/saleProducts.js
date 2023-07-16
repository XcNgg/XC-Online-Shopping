function getMySale() {
  $.ajax({
    url: "/users/GetMySale",
    method: "GET",
    success: function(response) {
      $('#sale-numbers').text(response.message);
      var productsLength = response.products.length;
      console.log("产品数量：" + productsLength);
      // 在这里进行其他逻辑操作，根据需要进行判断或处理
    },
    error: function(xhr, status, error) {
      console.error("请求出错：" + error);
    }
  });
}

$(document).ready(function() {
  getMySale(); // 页面加载时调用函数
});