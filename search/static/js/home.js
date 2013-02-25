$(function() {
    var $locationCombobox = $('#location-combobox');
    $locationCombobox .select2({width: 200});
    if (geoip_region) {
        var stateCode = geoip_region();
        if ($.type(stateCode) === 'string') {
            $locationCombobox.val(stateCode).trigger('change');
        }
    }

});