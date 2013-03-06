function submitRefine() {
    //construct object representing form state
    var refineForm = {};
    refineForm.q = ne.keyword;
    refineForm.l = ne.state;

    refineForm.ne = $('#refine-no-essay-required').prop('checked');
    refineForm.d = $('#refine-deadline').val();
    refineForm.e = $('#refine-ethnicity').val();
    refineForm.g = $('#refine-gender').val();
    var url = $.param(refineForm);
    window.location.href = '?' + url;

}
$(function() {
    var $datePicker = $('#refine-deadline').datepicker();
    //make refine form match page state
    $datePicker.datepicker('option', 'dateFormat', 'yy-mm-dd');
    $datePicker.val(ne.deadline);
    $('#refine-ethnicity').val(ne.ethnicity_restriction);
    $('#refine-gender').val(ne.gender_restriction);

    // wire up clickables
    $('#refine-submit').on('click', submitRefine);
});