// ==UserScript==
// @name        FogBugz Timesheet Hours
// @namespace   fb-ts-hours
// @description Calculate and display hours worked on FogBugz timesheet popup.
//              https://github.com/dimagi/commcarehq-scripts/blob/master/browser-scripts/FogBugz_Timesheet_Hours.user.js
// @include     http://manage.dimagi.com/*
// @version     2
// @grant       none
// ==/UserScript==
function main() {
    function calculateTimeWorked(table) {
        function date(value) {
            return new Date(TODAY + " " + value);
        }
        var NOW = new CTZNow(),
            TODAY = NOW.toDateString(),
            MINUTE = 60000,
            totalMinutes = 0,
            minutes;
        $.each(table.find("tr.row"), function(i, row) {
            var cells = $(row).find("td"),
                start = $("nobr", cells.get(2)).text(),
                end = $("nobr", cells.get(3)).text(),
                diff;
            if (end === "Stop Work") {
                diff = (NOW - date(start)) / MINUTE;
            } else {
                diff = (date(end) - date(start)) / MINUTE;
            }
            totalMinutes = totalMinutes + diff;
        });
        minutes = Math.floor(totalMinutes % 60);
        if (minutes < 10) {
            minutes = "0" + minutes;
        }
        return Math.floor(totalMinutes / 60) + ":" + minutes;
    }

    function setTimeWorked() {
        var table = $("#idTimesheetTable"),
            timeWorked = calculateTimeWorked(table),
            footer = $("#FBTH_timeWorked");
        if (footer.length === 0) {
            footer = $("<span id='FBTH_timeWorked' style='margin-left: 6em;'>");
            table.find("tr.row:last").next().find("th").append(footer);
        }
        footer.text(timeWorked);
    }

    var MutationObserver = window.MutationObserver || window.WebKitMutationObserver;
    var config = { childList: true, subtree: true };
    /**
     * Setup observer to invoke callback when child element is added to parent.
     *
     * Disconnect observer if callback returns true.
     */
    function onAddNode(child, parent, callback) {
        $(parent).each(function (x, target) {
            //console.log(target);
            var observer = new MutationObserver(function (mutations) {
                mutations.forEach(function (mutation) {
                    var nodes = mutation.addedNodes;
                    //console.log(nodes);
                    if (nodes && $(nodes).is(child)) {
                        if (callback(nodes)) {
                            observer.disconnect();
                        };
                    }
                });
            });
            observer.observe(target, config);
        });
    }

    onAddNode("#idTimesheetTable", "body", function() {
        setTimeWorked();

        // setup new observer on parent of #idTimesheetTable
        var parent = $("#idTimesheetTable").parent();
        onAddNode("#idTimesheetTable", parent, setTimeWorked);

        return true; // disconnect body observer (it's inefficient)
    });

    // Make the previous/next day buttons easier to click
    onAddNode("#idTimesheetTable", "body", function() {
        $('#timeclockPopup').css('top', '155px');
        $('#idTimesheetPrevious').css('padding', '.5em');
        $('#prevTimesheetButton').css('padding', '.5em');
        $('#idTimesheetNext').css('padding', '.5em');
        return true;
    });

    // Automatically click the "Schedule Items" dropdown
    $("#Menu_Working_On").click(function () {
        if ($("#idWorkingOnScheduleItem").css("display") === "none") {
            toggleWorkingOnCollapsible('idWorkingOnScheduleItem');
        }
    });

}

window.addEventListener('load', function() {
    if(typeof $ === 'undefined') {
        // load jQuery : http://stackoverflow.com/a/4261831/10840
        var script = document.createElement("script");
        script.setAttribute("src", "//ajax.googleapis.com/ajax/libs/jquery/1/jquery.min.js");
        script.addEventListener('load', function() {
            var script = document.createElement("script");
            script.textContent = "window.jQ=jQuery.noConflict(true);(" + main.toString() + ")();";
            document.body.appendChild(script);
        }, false);
        document.body.appendChild(script); 
    } else {
        main();
    }
});
