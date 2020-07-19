//hide Read, Analyze and Map divs initially
$('#read').hide();
$('#analyze').hide();
$('#map').hide();

$('#readbtn').click(function(){
    $('#read').show(); //show map div
    $('#analyze').hide(); //hide other divs
    $('#map').hide();
});

$('#sortbtn').click(function(){
    //sort
});


$('#analyzebtn').click(function(){
    $('#analyze').show(); //show analyze div
    $('#read').hide(); //hide other divs
    $('#map').hide();
});

$('#mapbtn').click(function(){
    $('#map').show(); //show map div
    $('#read').hide(); //hide other divs
    $('#analyze').hide();
    
    //create map
    var map = L.map('map').setView([51.0486,-114.0708], 11);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);
});