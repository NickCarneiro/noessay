function trackApplyClick() {
    var loggingParameters = {
        "schol_key": "{{ scholarship_key }}"
    }
    mixpanel.track("apply now clicked", loggingParameters);
}