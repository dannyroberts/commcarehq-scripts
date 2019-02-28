// ==UserScript==
// @name        Travis raw build link
// @namespace   dimagi
// @description Add link directly to raw log from build page
// @author      esoergel
// @include     http://travis-ci.org/*/builds/*
// @include     https://travis-ci.org/*/builds/*
// @require     http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js
// @grant       none
// ==/UserScript==

function addRawLogLinks () {
    $(".jobs-list > .jobs-item").each(function () {
        var link = $(this).find("a.ember-view").attr("href"),
            jobId = link.split("/").pop(),
            url = "https://api.travis-ci.org/v3/job/" + jobId + "/log.txt";
        $(this).prepend('<a class="button" href="' + url + '" ' +
                        'style="left: -5em; position: absolute;">Raw Log</a>');
    });
}

// Travis inserts the job nodes well after the page load finishes
// this is my incredibly hacky way of checking whether those exist yet
var JOB_ITEMS_EXIST = false;
var targetNode = document.querySelector("body");
var observerOptions = {
  childList: true,
  attributes: true,
  subtree: true
}
var observer = new MutationObserver(function (mutationList, observer) {
  if (!JOB_ITEMS_EXIST && $(".jobs-list > .jobs-item").length > 0) {
    JOB_ITEMS_EXIST = true;
    addRawLogLinks();
  }
});
observer.observe(targetNode, observerOptions);
