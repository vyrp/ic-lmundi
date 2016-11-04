$(function(){
    function rotateForEver($elem) {
        return $({deg: 0}).animate(
            {deg: 360},
            {
                duration: 2000,
                easing: "linear",
                step: function(now){
                    $elem.css({transform: "rotate(" + now + "deg)"});
                },
                complete: rotateForEver.bind(this, $elem)
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
        var $actionsCell = $(this).parent();
        var $tr = $actionsCell.parent();
        var id = $tr.data("id");
        var isNew = (id === "none");
        var $emailCell = $tr.children().first();
        var oldEmail = $emailCell.text();
        var $input = $('<input type="text" class="form-control" value="' + oldEmail + '">');
        $emailCell.html($input);
        $input.select();

        $input.keyup(function(event){
            switch (event.which) {
                case 13: // Enter
                    $emailCell.html($input.val());
                    // TODO:
                    //  1) enclose the two spans below in a div (this will help with the animation)
                    //  2) create a hidden html element with id="template", and clone it
                    $actionsCell.append(
                        '<span>&nbsp;&nbsp;&nbsp;</span>' +
                        '<span class="glyphicon glyphicon-refresh" aria-hidden="true"' +
                        'data-toggle="tooltip" data-placement="right" title="Sincronizando...">' +
                        '</span>');
                    var $indicator = $actionsCell.children().last().tooltip();
                    var $rotation = rotateForEver($indicator);
                    $.post({
                        url: "/ajax/emails/" + (isNew ? "add" : "edit"),
                        data: {
                            id: id,
                            value: $input.val()
                        },
                        success: function(data, textStatus, jqXHR){
                            if (isNew) {
                                $tr.data("id", data);
                            }

                            $rotation.stop();
                            changeTo($indicator, "ok", "green", "Sucesso");
                            setTimeout(function(){
                                $indicator.animate({width:"toggle"}, 300, function(){
                                    $indicator.remove();
                                    $actionsCell.children().last().remove();
                                });
                            }, 3000);
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
                case 27: // Esc
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
        var $actionsCell = $(this).parent();
        var $tr = $actionsCell.parent();
        var id = $tr.data("id");
        var email = $tr.children().first().text();

        // TODO: same as above
        $actionsCell.append(
            '<span>&nbsp;&nbsp;&nbsp;</span>' +
            '<span class="glyphicon glyphicon-refresh" aria-hidden="true"' +
            'data-toggle="tooltip" data-placement="right" title="Sincronizando...">' +
            '</span>');
        var $indicator = $actionsCell.children().last().tooltip();
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

    $(".glyphicon-pencil").click(pencilClickHandler);

    $(".glyphicon-trash").click(trashClickHandler);

    $(".plus-cell").click(function(){
        var $table = $(this).parents("tbody");
        // TODO:
        //  1) create hidden html element with id="template" and clone it
        //  2) use jinja macro to DRY
        var $newRow = $(
            '<tr data-id="none">' +
            '<td></td>' +
            '<td>' +
                '<span class="glyphicon glyphicon-pencil pointer" aria-hidden="true"></span>\n' +
                '<span>&nbsp;&nbsp;&nbsp;</span>\n' +
                '<span class="glyphicon glyphicon-trash pointer" aria-hidden="true"></span>' +
            '</td>' +
            '</tr>');
        $table.children("tr.active").before($newRow);
        $newRow.find(".glyphicon-pencil").click(pencilClickHandler).click();
        $newRow.find(".glyphicon-trash").click(trashClickHandler);
    });
});
