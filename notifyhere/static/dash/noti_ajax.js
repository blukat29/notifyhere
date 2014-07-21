function loadNoti(service) {
  var id = "#noti_" + service;
  $(id).html("Loading...");
  $.ajax({
    url:'/dash/ajax/' + service,
    type:'GET',
    success:function(result){
      $(id).html(result);
    }
  });
}
