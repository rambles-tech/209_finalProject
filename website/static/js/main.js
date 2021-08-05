function generateView() {
    // insert call to appropriate page here
    const page = window.location.href.split("?")[0].split("/spec")[0].replace(new RegExp("/+$"), "")

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

        const county_selector = document.querySelector('select[id="countySelect_0"]')
        const county = county_selector.options[county_selector.selectedIndex]

        const state_selector = document.querySelector('select[id="stateSelect_0"]')
        const state = state_selector.options[state_selector.selectedIndex]

        var countiesArr = []
        var numSelectors = document.querySelectorAll('select[class=stateSelectors').length;
        for (var i = 0; i < numSelectors; i++) {
            const county_selector = document.querySelector(`select[id="countySelect_${i}"]`)
            const county = county_selector.options[county_selector.selectedIndex].text

            const state_selector = document.querySelector(`select[id="stateSelect_${i}"]`)
            const state = state_selector.options[state_selector.selectedIndex].text
            countiesArr.push(`${county},${state}`)
        }

        var newPage = page + "/spec/" + array.join(";")
        if ((county.text !== "--") && (state.text !== "--"))  {
            newPage = newPage +
            "?reference_county=" + county.text + "&" +
            "reference_state=" + state.text + "&" +
            "counties_list=" + countiesArr.join("|")}
        console.log(newPage)
        window.location.href = newPage
    }
}

function removeAll(selectBox) {
    while (selectBox.options.length > 0) {
        selectBox.remove(0);
    }
}

function changeCounties(state, id, loc) {
  jQuery.getJSON(loc, function(json) {
    var selector = document.querySelector(`select[id="${id}"]`)

    //remove all counties currently in the
    //drop down select box
    removeAll(selector);

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

function createStateDropdown(data_loc) {
    //populate the state dropdown
    jQuery.getJSON(data_loc, function(json) {
    var numSelectors = document.querySelectorAll('select[class=stateSelectors').length;
    var countySelections = document.querySelector('div[id=countySelections]');
    var newSelectState = document.createElement("SELECT");
    var stateLabel = document.createElement("label");
    stateLabel.setAttribute("for", `stateSelect_${numSelectors}`);
    stateLabel.innerHTML = "State"
    newSelectState.setAttribute("id", `stateSelect_${numSelectors}`);
    newSelectState.setAttribute("class", "stateSelectors");
    newSelectState.setAttribute("onchange",
        onchange=`if (this.selectedIndex) changeCounties(this.options[this.selectedIndex].text, 'countySelect_${numSelectors}', '${data_loc}')`);
    newSelectState.innerHTML = "<option value='--'>--</option>";

    var newSelectCounty = document.createElement("SELECT");
    var countyLabel = document.createElement("label");
    countyLabel.setAttribute("for", `countySelect_${numSelectors}`);
    countyLabel.innerHTML = "County"
    newSelectCounty.setAttribute("id", `countySelect_${numSelectors}`);
    newSelectCounty.innerHTML = "<option value='--'>--</option>";

    countySelections.appendChild(stateLabel);
    countySelections.appendChild(newSelectState);
    countySelections.appendChild(countyLabel);
    countySelections.appendChild(newSelectCounty);
    countySelections.appendChild(document.createElement("br"));

    for (let s in json) {
        var opt = document.createElement('option');
        opt.value = s;
        opt.innerHTML = s;
        newSelectState.appendChild(opt);
    }

    persistReferenceCounty(newSelectState, newSelectCounty, numSelectors, json);
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

function persistReferenceCounty(stateSelect, countySelect, numSelector, json) {
  if (window.location.search) {
    var search = window.location.search.substring(1);
    var queryParams = JSON.parse('{"' + decodeURI(search).replace(/"/g, '\\"').replace(/&/g, '","').replace(/=/g,'":"') + '"}');
    var cList = queryParams["counties_list"].split("|");
    if (numSelector < cList.length) {
        const countyState = cList[numSelector].split(",")
        stateSelect.value = countyState[1];
        stateSelect.text = countyState[1];

        //remove all counties currently in the
        //drop down select box
        removeAll(countySelect);

        var opt = document.createElement('option');
        opt.value = '--';
        opt.innerHTML = '--';
        countySelect.appendChild(opt);

        console.log(json[countyState[1]])
        json[countyState[1]].forEach(c => {
            var opt = document.createElement('option');
            opt.value = c;
            opt.innerHTML = c;
            countySelect.appendChild(opt);
        })
        console.log(countySelect.options)
        countySelect.value = countyState[0];
        countySelect.text = countyState[0];
        }
    }
}
