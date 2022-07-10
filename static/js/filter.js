$(document).ready(function() {
    $('.messages').on('click', function(e) {
        e.preventDefault();
        $('.messages').hide();
    })

    $('.pixel-radio, .price-range-area, .order-sort, .season-sort').on('click change', function() {
        var _filterObj = {};
        var _lowerVal = $('#lower-value').html();
        var _upperVal = $('#upper-value').html();
        _filterObj.minPrice = _lowerVal;
        _filterObj.maxPrice = _upperVal;
        _filterObj.ordering = $('.order-sort option:selected').val()
        _filterObj.seasons = $('.season-sort option:selected').val()
        $('.pixel-radio').each(function(index, ele) {
            var _filterVal = $(this).val();
            var _filterKey = $(this).data('filter');
            _filterObj[_filterKey]=Array.from(document.querySelectorAll('input[data-filter=' + _filterKey + ']:checked')).map(function(el) {
                return el.value;
            });
        });
        // Run Ajax
        $.ajax({
            url: '/filter_data',
            data: _filterObj,
            dataType: 'json',
            beforeSend: function() {
                $('.ajaxLoader').show();
            },
            success: function(res) {
                $('#filteredProducts').html(res.data);
                $('.ajaxLoader').hide();
            }
        });
        // end
    });

    $('#load-color').on('click', function() {
        $.ajax({
            url: '/load_more/',
            success: function(res) {
                $('#colors').html(res.colors);
            }
        })
    })
})


