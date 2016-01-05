// ==UserScript==
// @name         GitHub open commits in tabs
// @namespace    github_open_commits
// @version      0.1
// @description  Open all commits in a PR in new tabs. https://github.com/dimagi/commcarehq-scripts/blob/master/browser-scripts/FogBugz_Timesheet_Hours.user.js
// @include      https://github.com/*/*/pull/*
// @require      http://ajax.googleapis.com/ajax/libs/jquery/2.1.0/jquery.min.js
// @grant        GM_openInTab
// ==/UserScript==
/* jshint -W097 */
'use strict';

$(document).ready(function() {
    var hrefs = new Array();
    var elements = $('.commit-id');
    elements.each(function() { 
        hrefs.push($(this).prop('href'))
    });

    $('.discussion-item-header').first().append('<input type="button" value="Open All Commits" id="CP">')
    $('#CP').css('float', 'right').addClass('btn').addClass('btn-sm');
    $('#CP').click(function(){ 
        $.each(hrefs, function(index, value) { 
            console.log(value);
            GM_openInTab(value);
        });
    });
});
