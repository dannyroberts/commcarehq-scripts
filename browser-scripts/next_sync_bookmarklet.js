// Add this as a bookmarklet and click it whenever you are trying to debug incremental syncs on the
// http://localhost/hq/admin/phone/restore/?as= page
javascript:(function(){var restore_id=document.getElementsByTagName('restore_id')[0].textContent,url=window.location.href,regex=/([\s\S]+)&since(=([^&#]*)|&|#|$)/,results=regex.exec(url),base_url=results[1],next_url=base_url+"&since="+restore_id;window.location.href=next_url;})();
