// 上传完图像，自动展示函数
function previewImage(input) {
    var file = input.files[0];
    var reader = new FileReader();
    reader.onload = function (e) {
        $('#preview_image').attr('src', e.target.result);
    }
    if (file) {
        reader.readAsDataURL(file);
    }
}


// 检查输入是否有效
function validateInputs() {
    var errorAlert = $('#error_alert');
    var successAlert = $('#success_alert');
    successAlert.hide();
    errorAlert.hide();

    // 检查产品名称
    var nameInput = $('#name');
    if (nameInput.val().trim() === '') {
        showError('产品名称不能为空');
        return false;
    }

    // 检查产品简述
    var simpleDescriptionInput = $('#simple_description');
    if (simpleDescriptionInput.val().trim() === '') {
        showError('产品简述不能为空');
        return false;
    }

    if (simpleDescriptionInput.length > 25) {
        showError('产品简述不能大于25个字');
        return false;
    }

    // 检查产品描述
    var descriptionInput = $('#description');
    if (descriptionInput.val().trim() === '') {
        showError('产品描述不能为空');
        return false;
    }

    // 检查产品价格
    var priceInput = $('#price');
    if (priceInput.val().trim() === '' || parseFloat(priceInput.val()) < 1) {
        showError('产品价格必须大于等于1');
        return false;
    }

    // 检查产品库存
    var stockInput = $('#stock');
    if (stockInput.val().trim() === '' || parseInt(stockInput.val()) < 0) {
        showError('产品库存必须大于等于0');
        return false;
    }

    return true;
}

// 显示错误
function showError(errorMessage) {
    var errorAlert = $('#error_alert');
    var successAlert = $('#success_alert');
    errorAlert.text(errorMessage).show();
    successAlert.hide();
}

// 显示成功！
function showSuccess(successMessage) {
    var errorAlert = $('#error_alert');
    var successAlert = $('#success_alert');
    successAlert.text(successMessage).show();
    errorAlert.hide();
}

function submitForm() {
    var errorAlert = $('#error_alert');
    var successAlert = $('#success_alert');
    var name = $('#name').val();
    var simpleDescription = $('#simple_description').val();
    var description = $('#description').val();
    var price = $('#price').val();
    var stock = $('#stock').val();
    var product_status = $('#product_status').val();
    var productType = $('#product_type').val();

    successAlert.hide();
    errorAlert.hide();
    // 判断图像如果不是默认的图像则进行审核
    if ($('#preview_image').attr('src') !== '/static/img/products/product.png') {
        var file = $('#logo_img')[0].files[0];
        var imgData = new FormData();
        imgData.append('logo_img', file);
        $.ajax({
            url: '/users/CheckSaleImg',
            type: 'POST',
            data: imgData,
            processData: false,
            contentType: false,
            success: function (response) {
                if (response.code !== 200) {
                    showError("图像不合规:"+response.message);
                    return false;
                } else {
                    showSuccess('图像审核通过！');
                    var img_src = response.filename;
                    var formData = new FormData();
                    formData.append('name', name);
                    formData.append('simple_description', simpleDescription);
                    formData.append('description', description);
                    formData.append('price', price);
                    formData.append('stock', stock);
                    formData.append('product_type', productType);
                    formData.append('img_src', img_src);
                    formData.append('product_status', product_status)

                    $.ajax({
                        url: '/users/AddMySale',
                        type: 'POST',
                        data: formData,
                        processData: false,
                        contentType: false,
                        success: function (response) {
                            if (response.code === 200) {
                                showSuccess('添加产品成功');
                                // 添加产品成功后的操作
                            } else {
                                showError(response.message);
                            }
                        },
                        error: function (xhr, status, error) {
                            showError('请求失败，请重试');
                        }
                    });
                }
            },
            error: function (xhr, status, error) {
                showError('出现错误！图像上传失败，请重试');
                return false;
            },
        });
    } else {
        var formData = new FormData();
        formData.append('name', name);
        formData.append('simple_description', simpleDescription);
        formData.append('description', description);
        formData.append('price', price);
        formData.append('stock', stock);
        formData.append('product_type', productType);
        formData.append('product_status', product_status);

        formData.append('img_src', '/static/img/products/product.png');
        $.ajax({
            url: '/users/AddMySale',
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function (response) {
                if (response.code === 200) {
                    showSuccess('添加产品成功');
                    // 添加产品成功后的操作
                } else {
                    showError(response.message);
                }
            },
            error: function (xhr, status, error) {
                showError('请求失败，请重试');
            }
        });
    }

}


$(document).ready(function () {
    // 上传完图像，自动展示
    $('#logo_img').on('change', function () {
        previewImage(this);
    });

    // 点击提交添加产品，则自动调用
    $('#AddSaleBtn').click(function () {
        if (validateInputs()) {
            // 验证并上传图像
            submitForm();
        }
    });
});



