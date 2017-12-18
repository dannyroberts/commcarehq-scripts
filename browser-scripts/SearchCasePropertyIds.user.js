// ==UserScript==
// @name         Search Case Property Ids
// @namespace    http://commcarehq.org/
// @version      0.2
// @description  Adds a link to search for IDs listed in case properties
// @author       frener
// @include      https://enikshay.in/a/*/reports/case_data/*/
// @include      https://*.commcarehq.org/a/*/reports/case_data/*/
// @grant        none
// ==/UserScript==

(function() {
    'use strict';
    var baseUrl = window.location.origin,
        tables = document.getElementsByClassName("property-table-container");
    for (var i = 0; i < tables.length; i++){
        var table = tables[i],
            els = table.getElementsByTagName('td');
        for(var j = 0; j < els.length; j++) {
            var el = els[j];
            el.innerHTML = el.innerText.replace(
                /^([0-9a-f]{8}-?[0-9a-f]{4}-?[0-9a-f]{4}-?[0-9a-f]{4}-?[0-9a-f]{12})/i,
                '$1 <a href="' + baseUrl + '/search/?q=$1" target="_blank"><i class="fa fa-search"></i></a>'
            );
        }
    }

})();
