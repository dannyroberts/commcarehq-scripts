// ==UserScript==
// @name         JIRA top comments box
// @namespace    dimagi
// @version      0.1
// @description  Moves the JIRA comments box to the top
// @author       Farid Rener
// @match        https://*.atlassian.net/browse/*
// @grant        none
// ==/UserScript==

(function() {
    'use strict';
    var issuePanel = document.getElementsByClassName('issuePanelWrapper')[0],
        commentsNode = document.getElementById('addcomment');
    issuePanel.parentNode.insertBefore(commentsNode, issuePanel);
})();
