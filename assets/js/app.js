

var $siteHeader = $('.site-header');

if($siteHeader.css("position") === "fixed"){
    $('.content').css('padding-top',$siteHeader.height()+'px');
}