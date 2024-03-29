function trackApplyClick() {
    var loggingParameters = {
        "schol_key": $('#apply-now').data('scholkey')
    }
    mixpanel.track("view_schol#applynow", loggingParameters);
}

$(function() {
     // wire up clickables
    $('#apply-now').on('click', trackApplyClick);

    // ne gets defined in footer_script.html
    mixpanel.track('view_schol', window['ne']);
});