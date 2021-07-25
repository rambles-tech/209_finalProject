function createStateDropdown(data_loc, id) {
    //populate the state dropdown
    jQuery.getJSON("{{ url_for('static', filename='data_sources/county_by_state_list.json') }}", function(json) {
    var selector = document.querySelector('select[id="stateSelect"]')

    for (let s in json) {
        var opt = document.createElement('option');
        opt.value = s;
        opt.innerHTML = s;
        selector.appendChild(opt);
    }
    });
}

// script will parse the URL, extract the everything after the final '/'
// then separate any parameters with ';']
function persistChecks() {
    const paramArr = window.location.href.split("/").slice(-1)[0].split("?")[0].split(";")

    //iterate through paramArr
    //set checked=true for respective parameters (checkboxes with corresponding variables)
    const checks = document.querySelectorAll('input[type=checkbox]')
    if (paramArr !== null) { checks.forEach(check => check.checked=(paramArr.includes(check.id))) };
}

function persistReferenceCounty() {
  if (window.location.search) {
    var search = window.location.search.substring(1);
    var queryParams = JSON.parse('{"' + decodeURI(search).replace(/"/g, '\\"').replace(/&/g, '","').replace(/=/g,'":"') + '"}');
    console.log(queryParams);
    document.getElementById("stateSelect").value = queryParams["reference_state"];
    changeCounties(queryParams["reference_state"]);
    document.getElementById("countySelect").value = queryParams["reference_county"];
  }
}

//var search = window.location.search.substring(1);
//var queryParams = JSON.parse('{"' + decodeURI(search).replace(/"/g, '\\"').replace(/&/g, '","').replace(/=/g,'":"') + '"}');
//console.log(queryParams);
//document.getElementById("stateSelect").val = queryParams["reference_state"];
persistReferenceCounty();