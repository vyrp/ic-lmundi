$(function(){
    function rotateForEver($elem, rotator) {
        if (rotator === void(0)) {
            rotator = $({deg: 0});
        } else {
            rotator.get(0).deg = 0;
        }

        return rotator.animate(
            {deg: 360},
            {
                duration: 2000,
                easing: "linear",
                step: function(now){
                    $elem.css({transform: "rotate(" + now + "deg)"});
                },
                complete: function(){
                    rotateForEver($elem, rotator);
                },
            }
        );
    }

    function changeTo($indicator, type, color, newTooltip) {
        $indicator.css({transform: "rotate(0deg)", color: color})
                  .removeClass("glyphicon-refresh")
                  .addClass("glyphicon-" + type)
                  .tooltip("hide")
                  .attr("data-original-title", newTooltip)
                  .tooltip("fixTitle");
    }

    function pencilClickHandler() {
        var $tr = $(this).parents("tr");
        var $emailCell = $tr.children().first();
        var $statusCell = $tr.children().last();
        var id = $tr.data("id");
        var isNew = (id === "new");
        var oldEmail = $emailCell.text();

        var $input = $('<input type="text" class="form-control" value="' + oldEmail + '">');
        $emailCell.html($input);
        $input.select();

        $input.keyup(function(event){
            switch (event.which) {
                case 13: // Key: Enter
                    var newEmail = $input.val();
                    $emailCell.html(newEmail);

                    // TODO:
                    //  1) enclose the two spans below in a div (this will help with the animation)
                    //  2) create a hidden html element with id="template", and clone it
                    var $indicator = $(
                        '<span class="glyphicon glyphicon-refresh" aria-hidden="true"' +
                        'data-toggle="tooltip" data-placement="right" title="Sincronizando...">' +
                        '</span>');
                    $statusCell.html($indicator);
                    $indicator.tooltip();
                    var $rotation = rotateForEver($indicator);

                    $.post({
                        url: "/ajax/emails/" + (isNew ? "add" : "edit"),
                        data: {
                            id: id,
                            value: newEmail
                        },
                        success: function(data, textStatus, jqXHR){
                            if (isNew) {
                                $tr.data("id", data);
                            }

                            $rotation.stop();
                            changeTo($indicator, "ok", "green", "Sucesso");
                            $indicator.delay(3000).fadeOut(300, $.fn.remove.bind($indicator));
                        },
                        error: function(jqXHR, textStatus, errorThrown){
                            $rotation.stop();
                            changeTo(
                                $indicator,
                                "remove",
                                "red",
                                "Erro: " + jqXHR.status + " " + errorThrown);
                            $emailCell.html(oldEmail);
                        }
                    });
                    break;
                case 27: // Key: Esc
                    if (isNew) {
                        $tr.remove();
                    } else {
                        $emailCell.html(oldEmail);
                    }
                    break;
            }
        });
    }

    function trashClickHandler() {
        var $statusCell = $(this).parent();
        var $tr = $statusCell.parent();
        var id = $tr.data("id");
        var email = $tr.children().first().text();

        // TODO: same as above
        $statusCell.append(
            '<span>&nbsp;&nbsp;&nbsp;</span>' +
            '<span class="glyphicon glyphicon-refresh" aria-hidden="true"' +
            'data-toggle="tooltip" data-placement="right" title="Sincronizando...">' +
            '</span>');
        var $indicator = $statusCell.children().last().tooltip();
        var $rotation = rotateForEver($indicator);
        $.post({
            url: "/ajax/emails/remove",
            data: {
                id: id
            },
            success: function(data, textStatus, jqXHR){
                $rotation.stop();
                $tr.remove();
            },
            error: function(jqXHR, textStatus, errorThrown){
                $rotation.stop();
                changeTo(
                    $indicator,
                    "remove",
                    "red",
                    "Erro: " + jqXHR.status + " " + errorThrown);
            }
        });
    }

    function addHandler() {
        var $table = $(this).parents("tbody");
        // TODO:
        //  1) create hidden html element with id="template" and clone it
        //  2) use jinja macro to DRY
        var $newRow = $(
            '<tr data-id="new">' +
            '<td></td>' +
            '<td>' +
                '<span class="glyphicon glyphicon-pencil pointer" aria-hidden="true"></span>\n' +
                '<span>&nbsp;&nbsp;&nbsp;</span>\n' +
                '<span class="glyphicon glyphicon-trash pointer" aria-hidden="true"></span>' +
            '</td>' +
            '<td></td>' +
            '</tr>');
        $table.children("tr.active").before($newRow);
        $newRow.find(".glyphicon-pencil").click(pencilClickHandler).click();
        $newRow.find(".glyphicon-trash").click(trashClickHandler);
    }

    $(".glyphicon-pencil").click(pencilClickHandler);

    $(".glyphicon-trash").click(trashClickHandler);

    $(".plus-cell").click(addHandler);
});
