jQuery(document).ready(function($) {
    $(".clickable-row").click(function() {
        window.document.location = $(this).attr("href");
    });

    $(".multi-select").multiSelect();

    $("#search").on("keyup", function() {
        var value = $(this).val();

        $("table.searchable tr").each(function(index) {
            if (index !== 0) {

                $row = $(this);

                var id = $row.find("td:first").text();

                if (id.indexOf(value) !== 0) {
                    $row.hide();
                }
                else {
                    $row.show();
                }
            }
        });
    });


});

