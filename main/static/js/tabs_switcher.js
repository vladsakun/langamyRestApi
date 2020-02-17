/**** JQuery *******/
jQuery('body').on('click','.next-tab', function(){
    var next = jQuery('.nav-tabs > .active').next('li');
    if(next.length){
        next.find('a').trigger('click');
    }else{
        jQuery('#myTabs a:first').tab('show');
    }
});

jQuery('body').on('click','.previous-tab', function(){
    var prev = jQuery('.nav-tabs > .active').prev('li')
    if(prev.length){
        prev.find('a').trigger('click');
    }else{
        jQuery('#myTabs a:last').tab('show');
    }
});