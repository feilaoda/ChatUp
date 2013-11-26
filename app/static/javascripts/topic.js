function replyatwho(name){
    var reply = $('#editor textarea');
    var oldv = reply.val();
    var prefix = name + " ";
    var newv = "";
    if(oldv.length>0){
        if (oldv != prefix) {
            newv = oldv + "\n" + prefix;
        }
    }else{
        newv = prefix;
    }
    reply.focus();
    reply.val(newv);
}
$(function(){
    $("div.hoverable").hover(function(){
      $(this).find("a.hoverable").show();
      },function(){
       $(this).find("a.hoverable").hide();
    });

    
});
