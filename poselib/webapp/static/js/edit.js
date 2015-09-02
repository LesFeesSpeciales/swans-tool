
function pausecomp(millis)
 {
  var date = new Date();
  var curDate = null;
  do { curDate = new Date(); }
  while(curDate-date < millis);
}

$('#reloadThumbnail').click(function(){
    //alert($(this).attr('pose'));
    var pose = $(this).attr('pose');
    connection.send('bpy.ops.lfs.pose_lib("EXEC_DEFAULT", action="SNAPSHOT", data="'+ pose + '")');
    pausecomp(400);
    location.reload();
});

$('#reloadPose').click(function(){
    //alert($(this).attr('pose'));
    var pose = $(this).attr('pose');
    var r = confirm("Are you sure you want to override the pose ?");
    if (r == true) {
        connection.send('bpy.ops.lfs.pose_lib("EXEC_DEFAULT", action="EXPORT_POSE", data="'+ pose + '")');
        pausecomp(200);
        location.reload();
    }
});

$('#reloadBoth').click(function(){
    //alert($(this).attr('pose'));
    var pose = $(this).attr('pose');
    var r = confirm("Are you sure you want to override the pose ?");
    if (r == true) {
        connection.send('bpy.ops.lfs.pose_lib("EXEC_DEFAULT", action="SNAPSHOT", data="'+ pose + '")');
        connection.send('bpy.ops.lfs.pose_lib("EXEC_DEFAULT", action="EXPORT_POSE", data="'+ pose + '")');
        pausecomp(700);
        location.reload();
    }
});

$('#applyPose').click(function(){
    //alert($(this).attr('pose'));
    var pose = $(this).attr('pose');
    var jsonPose =  btoa( $("#jsonPose").val() );  

    connection.send('bpy.ops.lfs.pose_lib("EXEC_DEFAULT", action="APPLY_POSE", data="'+ pose + '", jsonPose="' + jsonPose + '")');
    location.reload();
});


$('.saveChanges').change(function(){
    var pose = $(this).attr('pose');
    var value = $(this).val();

    $.ajax({
              method: "POST",
              url: "/edit" + pose,
              data: { title : value }
            })
              .done(function( msg ) {
                console.log( "Data Saved: " + msg );
              });
});