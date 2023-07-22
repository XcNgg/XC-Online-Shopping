var currentPage = 1; // 默认为第一页
var itemsPerPage = 15; // 每页显示的项数
var totalPages = 0; // 总页数

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
        data: {
            id: id,
            name: name
        },
        success: function(response) {
            $('#product-tables').hide();
            // 获取当前页的页码
            var activePage = currentPage;
            // 重新加载销售数据
            getMySale();
            // 处理成功响应
            if (response.code === 200) {
                toggleDiv(response.message, 1);
            } else {
                toggleDiv(response.message, 2);
            }
            // 恢复分页导航的激活状态
            setPaginationActive(activePage);
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

                    if (product.approval_status === 1) {
                        if (product.status === 1) {
                            row.append('<td><a class="btn btn-success" title="上架成功" href="#">上架成功</a></td>');
                        } else {
                            row.append('<td><a class="btn btn-secondary" title="努力备货中，赶紧上架吧！" href="#">努力备货</a></td>');
                        }
                    } else if (product.approval_status === 2) {
                        row.append('<td><a class="btn btn-danger" href="#" title="' + product.approval_info + '">审核失败</a></td>');
                    } else {
                        row.append('<td><a class="btn btn-warning" href="#" title="正在审核,请耐心等待">正在审核</a></td>');
                    }

                    row.append('<td>' + product.updated_at + '</td>');
                    row.append('<td><a href="/users/saleInfo?id='+ product.id +'">编辑</a></td>');
                    row.append('<td><a href="#" class="delete-button" data-name="' + product.name + '" data-id="' + product.id + '">删除</a></td>');
                    tableBody.append(row);
                }

                // 计算总页数
                totalPages = Math.ceil(productsLength / itemsPerPage);
                // 添加分页导航
                addPagination();
            } else {
                // 如果没有产品，显示相应提示
                $('#product-tables').hide();
                $('#pagination').empty(); // 清空分页导航
            }
        },
        error: function(xhr, status, error) {
            console.error("请求出错：" + error);
        }
    });
}

function addPagination() {
    // 生成分页导航的 HTML
    var paginationHtml = '';

    if (totalPages > 1) {
        paginationHtml += '<li class="page-item"><a class="page-link" href="#" data-page="prev">上一页</a></li>';
        for (var i = 1; i <= totalPages; i++) {
            paginationHtml += '<li class="page-item"><a class="page-link" href="#" data-page="' + i + '">' + i + '</a></li>';
        }
        paginationHtml += '<li class="page-item"><a class="page-link" href="#" data-page="next">下一页</a></li>';
    }

    // 显示分页导航
    $('#pagination').html(paginationHtml);

    // 添加分页导航的点击事件处理程序
    $('#pagination').on('click', 'li.page-item a.page-link', function() {
        var page = $(this).data('page');
        if (page === 'prev') {
            currentPage = Math.max(1, currentPage - 1);
        } else if (page === 'next') {
            currentPage = Math.min(totalPages, currentPage + 1);
        } else {
            currentPage = parseInt(page);
        }

        // 更新分页导航的激活状态
        setPaginationActive(currentPage);

        // 加载对应页的数据
        loadCurrentPageData();
    });

    // 默认显示第一页的数据和样式
    setPaginationActive(currentPage);
    loadCurrentPageData();
}

function setPaginationActive(activePage) {
    // 移除所有分页导航的激活状态
    $('#pagination li.page-item').removeClass('active');
    // 设置当前页的分页导航样式
    $('#pagination li.page-item').eq(activePage).addClass('active');
}

function loadCurrentPageData() {
    var start = (currentPage - 1) * itemsPerPage;
    var end = start + itemsPerPage;

    // 显示当前页的数据
    $('#product-tables tbody tr').hide();
    $('#product-tables tbody tr').slice(start, end).show();
}

$(document).ready(function() {
    getMySale(); // 页面加载时调用函数
});
