function redirect_login(){
  old = window.location.href;
  window.location.href="/account/signin?next="+old;
  return false;
}

function check_auth(){
  if(!logined){
    return redirect_login();
  }
  return true;
}

function sorting(url){
    var lis = $("#sortable li");
            var ids = [];
            for(var i=0; i<lis.length; i++) {
                 var id = lis[i].getAttribute('data-id');
                 ids.push(id);
            }
            $.ajax({
                url: url,
                type: 'POST',
                data:{ids:ids},
                dataType: 'json',
                timeout: 1000,
                error: function(){
                    //alert('Error sorting folders');
                },
                success: function(result){
                    // alert(result);
                }
                });

    return false;
}
