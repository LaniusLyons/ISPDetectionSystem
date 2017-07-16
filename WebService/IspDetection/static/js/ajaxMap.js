$.ajax({
    type: "GET",
    url: "/getIsp/",
    contentType:"text/plain",
    dataType:"json",
    success: function (data, status) {
        console.log(data);
    },
    error:function () {
        console.log('Error');
    }
});