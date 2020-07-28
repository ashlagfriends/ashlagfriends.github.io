

var $siteHeader = $('.site-header');

if($siteHeader.css("position") === "fixed"){
    $('.content').css('padding-top',$siteHeader.height()+'px');
} else {
    $('.content').css('padding-top','0px');
}

var lastScrollTop = 0;

$(window).scroll(function(event){
   var st = $(this).scrollTop();
   if(st > 100){
        if (st > lastScrollTop){
            //    גלילה למעלה
            $siteHeader.addClass('afterscroll');
            $('nav ul').addClass('hide');
            $("#pull i").removeClass("fa-times").addClass("fa-bars");
            // $siteHeader.css("position" ,"relative");
        } else {
            //    גלילה למטה
            $siteHeader.removeClass('afterscroll');
            // $siteHeader.css("position" ,"fixed");
        }
        lastScrollTop = st;
    }
});


var NextScroll = $(this).scrollTop();

$('a[href^="#"]').not('nav a').click(function () {

    $('html, body').animate({
        scrollTop: $('[name="' + $.attr(this, 'href').substr(1) + '"]').offset().top -20
    }, 500);
    return false;

    // if (lastScrollTop > NextScroll){
    //     $('html, body').animate({
    //         scrollTop: $('[name="' + $.attr(this, 'href').substr(1) + '"]').offset().top -20
    //     }, 500);
    //     return false;
    // } else {
    // $('html, body').animate({
    //     scrollTop: $('[name="' + $.attr(this, 'href').substr(1) + '"]').offset().top -20
    // }, 500);
    // return false;
    // }
});


// fa-times
$("#pull").click(function(){
    $("#pull i").toggleClass("fa-bars").toggleClass("fa-times");
  });

// fa-bars