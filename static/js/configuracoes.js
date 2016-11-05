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

    function changeTo($span, type, color, newTooltip) {
        $span.css({transform: "rotate(0deg)", color: color})
                  .removeClass("glyphicon-refresh")
                  .addClass("glyphicon-" + type)
                  .tooltip("hide")
                  .attr("data-original-title", newTooltip)
                  .tooltip("fixTitle");
    }

    function createIndicator($statusCell) {
        var $span = $(
            '<span class="glyphicon glyphicon-refresh" aria-hidden="true" data-html="true"' +
            'data-toggle="tooltip" data-placement="top" title="Sincronizando...">' +
            '</span>');
        $statusCell.html($span);
        $span.tooltip();
        return {
            span: $span,
            rotation: rotateForEver($span)
        };
    }

    function indicatorToRedCross(indicator) {
        return function(jqXHR, textStatus, errorThrown) {
            indicator.rotation.stop();
            changeTo(
                indicator.span,
                "remove",
                "red",
                "Error: " + jqXHR.status + " " + errorThrown + "<br/>(" + jqXHR.responseText + ")");
        };
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

        function reset() {
            if (isNew) {
                $tr.remove();
            } else {
                $emailCell.html(oldEmail);
            }
        }

        $input.keyup(function(event){
            switch (event.which) {
                case 13: // Key: Enter
                    var newEmail = $input.val();
                    $emailCell.html(newEmail);

                    var indicator = createIndicator($statusCell);
                    var $span = indicator.span;
                    var $rotation = indicator.rotation;

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
                            changeTo($span, "ok", "green", "Sucesso");
                            $span.delay(3000).fadeOut(300, $.fn.remove.bind($span));
                        },
                        error: [indicatorToRedCross(indicator), reset]
                    });
                    break;
                case 27: // Key: Esc
                    reset();
                    break;
            }
        });
    }

    function trashClickHandler() {
        var $tr = $(this).parents("tr");
        var indicator = createIndicator($tr.children().last());

        $.post({
            url: "/ajax/emails/remove",
            data: {
                id: $tr.data("id")
            },
            success: function(data, textStatus, jqXHR){
                $tr.remove();
            },
            error: indicatorToRedCross(indicator)
        });
    }

    function addHandler() {
        var $table = $(this).parents("tbody");
        var $newRow = $("#row-template").clone().show();
        $table.children("tr.active").before($newRow);
        $newRow.find(".glyphicon-pencil").click(pencilClickHandler).click();
        $newRow.find(".glyphicon-trash").click(trashClickHandler);
    }

    $(".glyphicon-pencil").click(pencilClickHandler);

    $(".glyphicon-trash").click(trashClickHandler);

    $(".plus-cell").click(addHandler);
});
