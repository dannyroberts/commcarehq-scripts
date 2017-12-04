// ==UserScript==
// @name         Search Case Property Ids
// @namespace    http://commcarehq.org/
// @version      0.1
// @description  Adds a link to search for IDs listed in case properties
// @author       frener
// @include      https://enikshay.in/a/*/reports/case_data/*/
// @include      https://*.commcarehq.org/a/*/reports/case_data/*/
// @grant        none
// ==/UserScript==

(function() {
    'use strict';
    var baseUrl = window.location.origin,
        els = document.getElementsByTagName("td");
    for(var i = 0, l = els.length; i < l; i++) {
        var el = els[i];
        el.innerHTML = el.innerText.replace(
            /([0-9a-f]{8}-?[0-9a-f]{4}-?[0-9a-f]{4}-?[0-9a-f]{4}-?[0-9a-f]{12})/i,
            '$1 <a href="' + baseUrl + '/search/?q=$1" target="_blank"><i class="fa fa-search"></i></a>'
        );
    }
})();
