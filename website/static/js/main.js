function generateView() {
    // insert call to appropriate page here
    const page = window.location.href.split("spec")[0]

    //following code checks all checkboxes for state
    //creates array with id names of all checked boxes
    var array = []
    var checkboxes = document.querySelectorAll('input[type=checkbox]:checked')

    if (checkboxes.length == 0) {
        alert("Select at least one data field.");
    }
    else {
        for (var i = 0; i < checkboxes.length; i++) {
        array.push(checkboxes[i].id)
        }

        const county_selector = document.querySelector('select[id="countySelect"]')
        const county = county_selector.options[county_selector.selectedIndex]

        const state_selector = document.querySelector('select[id="stateSelect"]')
        const state = state_selector.options[state_selector.selectedIndex]

        var newPage = page + "spec/" + array.join(";")
        if ((county.text !== "--") && (state.text !== "--"))  { newPage = newPage + "?reference_county=" + county.text + "&" + "reference_state=" + state.text}
        console.log(newPage)
        window.location.href = newPage
    }
}

function changeCounties(state, loc) {
  jQuery.getJSON(loc, function(json) {
    var selector = document.querySelector('select[id="countySelect"]')

    jQuery("#countySelect").empty();

    var opt = document.createElement('option');
    opt.value = '--';
    opt.innerHTML = '--';
    selector.appendChild(opt);

    console.log(json[state])
    json[state].forEach(c => {
        var opt = document.createElement('option');
        opt.value = c;
        opt.innerHTML = c;
        selector.appendChild(opt);
    })
  });
}

function createStateDropdown(data_loc, id) {
    //populate the state dropdown
    jQuery.getJSON(data_loc, function(json) {
    var countySelections = document.querySelector('div[id=countySelections]')
    var newSelectState = document.createElement("SELECT");
    newSelectState.setAttribute("id", "stateSelect"+id);
    countySelections.appendChild(newSelectState);

//    var selector = document.querySelector('select[id="stateSelect"+id]')

    for (let s in json) {
        var opt = document.createElement('option');
        opt.value = s;
        opt.innerHTML = s;
        newSelectState.appendChild(opt);
    }
    });
}

function selectAllChecks() {
    const paramArr = window.location.href.split("/").slice(-1)[0].split("?")[0].split(";");
    const checks = document.querySelectorAll('input[type=checkbox]');
    checks.forEach(check => check.checked=true);
}

function clearAllChecks() {
    const paramArr = window.location.href.split("/").slice(-1)[0].split("?")[0].split(";");
    const checks = document.querySelectorAll('input[type=checkbox]');
    checks.forEach(check => check.checked=false);
}

// script will parse the URL, extract the everything after the final '/'
// then separate any parameters with ';']
function persistChecks() {
    const paramArr = window.location.href.split("/").slice(-1)[0].split("?")[0].split(";");
    const checks = document.querySelectorAll('input[type=checkbox]');
    if (paramArr !== "") { checks.forEach(check => check.checked=(paramArr.includes(check.id))) };
}

function persistReferenceCounty() {
  if (window.location.search) {
    var search = window.location.search.substring(1);
    var queryParams = JSON.parse('{"' + decodeURI(search).replace(/"/g, '\\"').replace(/&/g, '","').replace(/=/g,'":"') + '"}');
    console.log(queryParams);
    var stateSelect = document.querySelector('select[id="stateSelect"]');
    stateSelect.value = queryParams["reference_state"];
    changeCounties(queryParams["reference_state"]);
    document.getElementById("countySelect").value = queryParams["reference_county"];
  }
}

//var search = window.location.search.substring(1);
//var queryParams = JSON.parse('{"' + decodeURI(search).replace(/"/g, '\\"').replace(/&/g, '","').replace(/=/g,'":"') + '"}');
//console.log(queryParams);
//document.getElementById("stateSelect").val = queryParams["reference_state"];
//persistReferenceCounty();