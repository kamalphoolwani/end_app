var isStarted = false

function init() {
    console.log('init called')
    sessionStorage.setItem("user", "{{ username }}")
    $('#cameras').hide();
    $('#attendance').hide();
    $('#attentive').hide();
    $('#activator').hide();
    $('#default_error').hide();

        // $('#plots').find('tr').not('#table_header').hide();
        // $('#plots').find('#plot_segment1').show();
}

function home() {
    $('#home').show();
    $('#attendance').hide();
    $('#attentive').hide();
    $('#activator').hide();
    $('#default_error').hide();
}

function attendance() {
    if (!isStarted)
        display_error()
    else {
        $('#home').hide();
        $('#attendance').show();
        $('#attentive').hide();
        $('#activator').hide();
        $('#default_error').hide();
    }
}

function attentive() {
    if (!isStarted)
        display_error()
    else {
        $('#home').hide();
        $('#attendance').hide();
        $('#attentive').show();
        $('#activator').hide();
        $('#default_error').hide();
    }
}

function activator() {
    if (!isStarted)
        display_error()
    else {
        $('#home').hide();
        $('#attendance').hide();
        $('#attentive').hide();
        $('#activator').show();
        $('#default_error').hide();
    }
}

function start_class() {
    isStarted = true
    get_images()
    $('#cameras').show();

}

function end_class() {
    isStarted = false
    clearInterval(get_img_interval)
    $('#camera1').find('img').attr('src', './static/default.jpg');
    $('#camera2').find('img').attr('src', './static/default.jpg');
    $('#camera3').find('img').attr('src', './static/default.jpg');
    $('#cameras').hide();
}

function get_images() {

    if (isStarted) {
        $.ajax({
            type: "GET",

            url: "/get_updates",
            data: '',
            success: function (data) {
                console.log('inside success',data)
                $('#camera1').find('img').attr('src', './static/cam1.jpg');
                $('#camera2').find('img').attr('src', './static/cam2.jpg');
                $('#camera3').find('img').attr('src', './static/cam3.jpg');
                $('#attendance').find('tbody').empty()
                var idx=1;
                for (const [key, value] of Object.entries(data['attend'])) {
                    console.log(key, value);
                    $('#attendance').find('tbody').append($('<tr>')
                    .append($('<th>').append(idx++))
                    .append($('<td>').append(key))
                    .append($('<td>').append(value==0?'Absent':'Present'))
                  )
                }
                drawChart(data['attentive'])
            }
        });
    }
}

get_img_interval=setInterval(function() {
    get_images() // this will run after every 5 seconds
}, 35000);

function logout() {
    end_class()
    window.location = 'logout'
}

function display_error() {
    $('#home').hide();
    $('#attendance').hide();
    $('#attentive').hide();
    $('#activator').hide();
    $('#default_error').show();
}

function check_session() {

}

google.charts.load('current', {'packages':['corechart']});
// google.charts.setOnLoadCallback(drawChart);

// Draw the chart and set the chart values
function drawChart(a) {
  var data = google.visualization.arrayToDataTable([
  ['Label', 'Percentage'],
  ['Attentive', a],
  ['Non-Attentive', 100-a]
]);

  // Optional; add a title and set the width and height of the chart
  var options = {'title':'Class Attentiveness', 'width':550, 'height':400};

  // Display the chart inside the <div> element with id="piechart"
  var chart = new google.visualization.PieChart(document.getElementById('piechart'));
  chart.draw(data, options);
}