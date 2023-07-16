function getMySale() {
  $.ajax({
    url: "/users/GetMySale",
    method: "GET",
    success: function(response) {
      $('#sale-numbers').text(response.message);
      var products = response.products;
      var productsLength = products.length;

      if (productsLength > 0) {
        $('#product-tables').show();
        var tableBody = $('#product-tables tbody');
        tableBody.empty(); // 清空表格内容

        // 遍历产品列表，生成表格行
        for (var i = 0; i < productsLength; i++) {
          var product = products[i];
          var row = $('#tbody');
          row.append('<tr>')
          row.append('<th scope="row">' + (i + 1) + '</th>');
          row.append('<th scope="row">' + product.id + '</th>');
          row.append('<td>' + product.name + '</td>');
          row.append('<td><img src="' + product.logo_img + '" alt="logo" style="display: inline-block; vertical-align: top;" width="20" height="20"></td>');
          row.append('<td>' + product.price + '</td>');
          row.append('<td>' + product.sales + '</td>');
          row.append('<td>' + product.stock + '</td>');
          row.append('<td>' + product.product_type + '</td>');
          row.append('<td>' + product.created_at + '</td>');
          row.append('<td>' + product.updated_at + '</td>');
          row.append('<td><a href="#">编辑</a></td>');
          row.append('<td><a href="#">删除</a></td>');
          row.append('</tr>')
          tableBody.append(row);
        }
      } else {
        $('#product-tables').hide();
      }

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
