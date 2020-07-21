jQuery(document).ready(function($) {

    var $wpAdminBar = $('#wpadminbar');
    var $siteHeader = $('#site-header');   
            
            if ($wpAdminBar.length) {
                // אם יש גודל לאדר של אוורדפרס
                if($wpAdminBar.css("position") === "fixed"){
                    // האם לאדר של אוורדפרס יש פיקס 
                    $siteHeader.css({"position":"fixed"});
                    $siteHeader.css('top',$wpAdminBar.height()+'px');
                    $('#main').css('padding-top',$siteHeader.height()+'px');
                } else {
                    $(window).on('scroll', function () {            
                          var headerHeight = $wpAdminBar.outerHeight();
                          if ($(window).scrollTop() > headerHeight) {
                              $siteHeader.css({"position":"fixed" , "top":"0"});
                              $('#main').css('padding-top',$siteHeader.height()+'px'); 
                          } else {                            
                                $siteHeader.css({"position":"relative"});
                                $('#main').css({"padding-top":"0"});                          
                          }
                    });
                }
            } else {
                $siteHeader.css({"position":"fixed" , "top":"0"});
                $('#main').css('padding-top',$siteHeader.height()+'px');            
            }   


});