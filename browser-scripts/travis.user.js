// ==UserScript==
// @name        Travis raw build link
// @namespace   dimagi
// @description Add link directly to raw log from build page
// @author      esoergel
// @include     http://travis-ci.org/*/builds/*
// @include     https://travis-ci.org/*/builds/*
// @grant       none
// ==/UserScript==

(function () {
    'use strict';
    $(".jobs-list > .jobs-item").each(function () {
        var link = $(this).find("a.ember-view").attr("href"),
            jobId = link.split("/").pop(),
            url = "https://api.travis-ci.org/v3/job/" + jobId + "/log.txt";
        $(this).prepend('<a class="button" href="' + url + '" ' +
                        'style="left: -5em; position: absolute;">Raw Log</a>');
    });
})();
