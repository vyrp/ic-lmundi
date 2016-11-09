$(function(){
    var email_regex = /^[-a-z0-9~!$%^&*_=+}{\'?]+(\.[-a-z0-9~!$%^&*_=+}{\'?]+)*@([a-z0-9_][-a-z0-9_]*(\.[-a-z0-9_]+)*\.(aero|arpa|biz|com|coop|edu|gov|info|int|mil|museum|name|net|org|pro|travel|mobi|[a-z][a-z])|([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}))(:[0-9]{1,5})?$/i;

    $confModal = $("#confirmation-modal");
    $deleteSureBtn = $("#delete-item-sure");

    $confModal.on("hidden.bs.modal", function(){
        $deleteSureBtn.off("click");
    });

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

    function isValid(newValue, category) {
        if (category === "emails") {
            return email_regex.test(newValue);
        }
        return true;
    }

    function pencilClickHandler() {
        var $tr = $(this).parents("tr");
        var $valueCell = $tr.children().first();
        var $statusCell = $tr.children().last();
        var id = $tr.data("id");
        var category = $tr.parents(".tab-pane").get(0).id;
        var isNew = (id === "new");
        var oldValue = $valueCell.text();

        var $input = $('<input type="text" class="form-control" value="' + oldValue + '">');
        $valueCell.html($input);
        $input.select();

        function reset() {
            if (isNew) {
                $tr.remove();
            } else {
                $valueCell.html(oldValue);
            }
        }

        $input.keyup(function(event){
            switch (event.which) {
                case 13: // Key: Enter
                    var newValue = $input.val().trim();

                    if (isValid(newValue, category)) {
                        $valueCell.removeClass("has-error");
                    } else {
                        $valueCell.addClass("has-error");
                        break;
                    }

                    $valueCell.html(newValue);

                    var indicator = createIndicator($statusCell);
                    var $span = indicator.span;
                    var $rotation = indicator.rotation;

                    $.post({
                        url: "/ajax/" + category + "/" + (isNew ? "add" : "edit"),
                        data: {
                            id: id,
                            value: newValue
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

        $deleteSureBtn.click(function(){
            var indicator = createIndicator($tr.children().last());
            var category = $tr.parents(".tab-pane").get(0).id;

            $.post({
                url: "/ajax/" + category + "/remove",
                data: {
                    id: $tr.data("id")
                },
                success: function(data, textStatus, jqXHR){
                    $tr.remove();
                },
                error: indicatorToRedCross(indicator)
            });

            $confModal.modal("hide");
        });

        $confModal.modal("show");
    }

    function addHandler() {
        var $table = $(this).parents("tbody");
        var $newRow = $("#row-template").clone().attr("id", "").show();
        $table.children("tr.active").before($newRow);
        $newRow.find(".glyphicon-pencil").click(pencilClickHandler).click();
        $newRow.find(".glyphicon-trash").click(trashClickHandler);
    }

    $(".glyphicon-pencil").click(pencilClickHandler);
    $(".glyphicon-trash").click(trashClickHandler);
    $(".plus-cell").click(addHandler);
});
