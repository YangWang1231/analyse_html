var temp_str ='<img src="file://C:\\LDRA_Toolsuite\\images/';
var base_str ='<a href="file://C:\\LDRA_Toolsuite\\';
var ie_ver = getIE_ver();
function getIE_ver()
{
var ret = -1;
if (navigator.appName == 'Microsoft Internet Explorer')
{
var ua = navigator.userAgent;
var re = new RegExp("MSIE ([0-9]{1,}[\.0-9]{0,})");
if (re.exec(ua) != null)
{
ret = parseFloat( RegExp.$1 );
}
}
return ret;
}
