  $(document).ready(function () {
        // 页面加载完成后，获取数据并渲染产品卡片
        fetchDataAndRender();
        $('#loading-spinner-message').hide();


});


$('.more-img').click(function() {
    $('#loading-spinner-message').show();
});

    function fetchDataAndRender(page=1,keyword='',type='虚拟产品') {
        $('#loading-spinner-message').show();
        // 发送请求获取数据
        var apiUrl = `/products/getproduct?keyword=${keyword}&page=${page}&type=${type}`;
        $.get(apiUrl, function (response) {
            if (response.code === 200) {
                var productsData = response.data;
                // 渲染产品卡片
                renderProductCards(productsData);
                $('#loading-spinner-message').hide();
            } else {
                $('#loading-spinner-message').hide();
                console.log('Error fetching product data.');
            }
        });
    }

    function renderProductCards(productsData) {
        var productContainer = $('#product-list');
        // 清空原有的内容
        productContainer.empty();
        // 循环渲染每个产品卡片
        for (var i = 0; i < productsData.length; i++) {
            var product = productsData[i];

            var productCardHtml = `
                <div class="col-md-3 mb-2">
                    <div class="card">
                        <div class="card-body" style="height:240px;">
                            <div class="row">
                                <div class="col-4" style="height:50px;">
                                    <img src="${product.img_src}" class="img-thumbnail rounded card-img-top"
                                         alt="Product 1" style="max-width: 100%; display: block; margin: 0 auto;">
                                </div>

                                <div class="col-8" style="height:125px;">
                                    <h5 class="card-title">${product.name}</h5>
                                    <p>${product.simple_description}</p>
                                </div>
                            </div>
                            <!-- 其他产品信息的渲染 -->
                                <div class="row">
                                    <div class="col-6">
                                        <img src="/static/img/products/RMB.png"
                                             alt="RMB"
                                             style="display: inline-block; vertical-align: middle;" width="18"
                                             height="15">
                                        <span id="product-RMB">${product.price}</span>
                                    </div>
                                    <div class="col-6">
                                        <img src="/static/img/products/type.png"
                                             alt="分类"
                                             style="display: inline-block; vertical-align: middle;" width="18"
                                             height="15">
                                        <span id="product-type">${product.product_type}</span>
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-6">
                                        <img src="/static/img/products/sales-volume.png"
                                             alt="销量"
                                             style="display: inline-block; vertical-align: middle;" width="18"
                                             height="15">
                                        <span id="product-sales-volume">${product.sales}</span>
                                    </div>
                                    <div class="col-6">
                                        <img src="/static/img/products/inventory.png"
                                             alt="库存"
                                             style="display: inline-block; vertical-align: middle;" width="18"
                                             height="15">
                                        <span id="product-inventory">${product.stock}</span>
                                    </div>
                                </div>
                                <a href="/products/productinfo?id=${product.id}"
                                   style="color:#8a8a8a;text-align: right; float: right; text-decoration: none;">
                                    more
                                    <img class="more-img" src="/static/img/products/more.png"
                                         alt="了解更多"
                                         style="display: inline-block; vertical-align: middle;" width="18"
                                         height="15">
                                </a>
                        </div>
                    </div>
                </div>
            `;
            productContainer.append(productCardHtml);
        }
            // console.log(productCardHtml);
            // console.log(productContainer);

    }