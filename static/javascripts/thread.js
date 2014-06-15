function newthread(id){
    var c = $("#content").val();
    $.ajax({
        url: "/group/"+id+"/new",
        type: 'POST',
        data:{content:c},
        dataType: 'json',
        timeout: 1000,
        error: function(){
            alert('Error sorting folders');
        },
        success: function(result){
           alert(ok);
        }
        });


}