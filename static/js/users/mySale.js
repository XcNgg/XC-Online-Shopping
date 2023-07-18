function toggleDiv(divValue, divType) {
    if (divType === 2) {
        $('#error_alert').text(divValue).show();
        $('#success_alert').hide();
    } else if (divType === 1) {
        $('#success_alert').text(divValue).show();
        $('#error_alert').hide();
    }
}

$(document).on('click', '.delete-button', function() {
  var id = $(this).data('id');
  var name = $(this).data('name');
  $.ajax({
    url: "/users/DeleteMySale",
    method: "POST",
    data:
        {
          id:id,
          name: name
        },
    success: function(response) {
        $('#product-tables').hide();
        // 重新加载销售数据
        getMySale();
      // 处理成功响应
      if (response.code===200){
          toggleDiv(response.message,1);
      }else{
        toggleDiv(response.message,2);
      }
    },
    error: function(xhr, status, error) {
      // 处理错误
      console.error("请求出错：" + error);
    }
  });
});

function getMySale() {
  $.ajax({
    url: "/users/GetMySale",
    method: "GET",
    success: function(response) {
      $('#sale-numbers').text(response.message);
      var products = response.data;
      var productsLength = products.length;
      if (productsLength > 0) {
        $('#product-tables').show();
        var tableBody = $('#product-tables tbody');
        tableBody.empty(); // 清空表格内容

        // 遍历产品列表，生成表格行
        for (var i = 0; i < productsLength; i++) {
          var product = products[i];
          var row = $('<tr class="text-center">');
          row.append('<th scope="row">' + (i + 1) + '</th>');
          row.append('<td>' + product.name + '</td>');
          row.append('<td><img src="' + product.img_src + '" alt="logo" style="display: inline-block; vertical-align: top;" width="20" height="20"></td>');
          row.append('<td>' + product.price + '</td>');
          row.append('<td>' + product.sales + '</td>');
          row.append('<td>' + product.stock + '</td>');
          row.append('<td>' + product.product_type + '</td>');

          if(product.approval_status === 1 ){
              if (product.status === 1){
                row.append('<td><a class="btn btn-success" title="上架成功" href="#">上架成功</a></td>');
              }else {
                  row.append('<td><a class="btn btn-secondary" title="努力备货中，赶紧上架吧！" href="#">努力备货</a></td>');
              }
          }else if(product.approval_status === 2){
              row.append('<td><a class="btn btn-danger" href="#" title="'+product.approval_info+'">审核失败</a></td>');
          }else{
                row.append('<td><a class="btn btn-warning" href="#" title="正在审核,请耐心等待">正在审核</a></td>');
          }

          row.append('<td>' + product.updated_at + '</td>');
          row.append('<td><a href="#">编辑</a></td>');
          row.append('<td><a href="#" class="delete-button" data-name="' + product.name + '" data-id = "'+ product.id +'">删除</a></td>');
          tableBody.append(row);
        }
      } else {

      }

      // console.log("产品数量：" + productsLength);
      // 在这里进行其他逻辑操作，根据需要进行判断或处理
    },
    error: function(xhr, status, error) {
      // console.error("请求出错：" + error);
    }
  });
}

$(document).ready(function() {
  getMySale(); // 页面加载时调用函数
});
