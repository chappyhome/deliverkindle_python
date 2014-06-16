var feedbackToggle;

(function($){

feedbackToggle = function(){
	$('#feedback_tab, #feedback_panel').toggle();
}

$(document).ready(function(){
	$('#feedback_tab button, #feedback_panel button').click(feedbackToggle);

    $( document ).on("click","#feedback_panel li a[href='#']",function(){
        var favorites_id = $(this).attr('favorites_id');
        var node_id = '#mybookdiv' + favorites_id;      
        //alert($(this).attr('book_id');

        if(!confirm('你确定要删除吗?')) return false;
       
        var action = '/favorites/delete/' + favorites_id;
        $.ajax({'url': action, 
            'type': 'get',
            'data': '',
            'success': function(data, textStatus, jqXHR){
                        $(node_id).remove();
                        if($(".lid").length == 1 && $(".bookdiv center").length ==0 ){
                              var html = '<center>你的收藏为空.</center>';
                              $("#feedback_panel #insert_tag").before(html);
                        }         
        },
        'error': function(jqXHR, textStatus, errorThrown){
            if (jqXHR.status == 400)
            {
                var errors = "The following field error(s) ocurred: \n";
                errors += jqXHR.responseText;
                alert(errors);
            }
            else if(jqXHR.responseText != ''){
                alert("The following error ocurred: \n"+jqXHR.responseText);
            }
            else{
                alert('An unknown error occurred.');
            }
        }
        });
    });


});

})(jQuery);
