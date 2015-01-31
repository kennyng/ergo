// popup sidebar
$( document ).on( "pageinit", function() {
           
    $( ".sidebarPopup" ).on({
        popupbeforeposition: function() {
            var h = $( window ).height();
        
            $( ".sidebarPopup" )
                .css( "height", h );
        }
    });
     
    $( ".sidebarPopup button" ).on( "click", function() {
        $( ".sidebarPopup" ).popup('close');
    });

});