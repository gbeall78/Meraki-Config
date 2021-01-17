function updateOrg(orgID) {
    $.ajax({
        type: "get",
        url: $SCRIPT_ROOT + '/updateOrg',
        data: {
            orgID: orgID,
        },
        success: function(response) {
            window.location.href = "/updateSuccess";
        }
    });
}