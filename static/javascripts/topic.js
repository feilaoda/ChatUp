function redirect_login(){
  old = window.location.href;
  window.location.href="/account/signin?next="+old;
  return false;
}
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


function star_wist(id, url){
    var url = "/wist/"+id+"/star";
    $.ajax({
        url: url,
        type: 'POST',
        dataType: 'json',
        crossDomain: true,
        timeout: 1000,
        error: function(req,status){
            if(req.status == '403') {
                redirect_login();
            }
        },
        success: function(json){
            if(json.result == '403'){
                redirect_login();
            }

            if(json.result != '200'){
                var count = json.data.count;
                $("#star_count").html(count);
            }else{
                var count = json.data.count;
                $("#star_count").html(count);
                $("#star_btn").html('Unstar');
                $("#star_btn").attr('onclick',"unstar_wist('"+id+"')");
            }
        }
    });

    return false;
}

function unstar_wist(id){
    var url = "/wist/"+id+"/unstar";
    $.ajax({
        url: url,
        type: 'POST',
        dataType: 'json',
        crossDomain: true,
        timeout: 1000,
        error: function(req,status){
            if(req.status == '403') {
                redirect_login();
            }
        },
        success: function(json){
            if(json.result == '403'){
                redirect_login();
            }

            if(json.result != '200'){
                var count = json.data.count;
                $("#star_count").html(count);
            }else{
                var count = json.data.count;
                $("#star_count").html(count);
                $("#star_btn").html('Star');
                $("#star_btn").attr('onclick',"star_wist('"+id+"')");
            }
        }
    });

    return false;
}

