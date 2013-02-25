$(document).ready(function() {
    var $locationCombobox = $('#location-combobox');
    $locationCombobox.select2({width: 180});
    $locationCombobox.val(ne.state).trigger('change');
});