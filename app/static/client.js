var el = x => document.getElementById(x);

function analyze() {
  el("analyze-button").innerHTML = "Analyzing...";
  var xhr = new XMLHttpRequest();
  var loc = window.location;
  xhr.open("POST", `${loc.protocol}//${loc.hostname}:${loc.port}/analyze`,
    true);
  xhr.onerror = function() {
    alert(xhr.responseText);
  };
  xhr.onload = function(e) {
    if (this.readyState === 4) {
      var response = JSON.parse(e.target.responseText);
      if (response["result"] == "1") {
        el("result-label").innerHTML = `This text belongs to comp.graphics`;
      } else if (response["result"] == "7") {
        el("result-label").innerHTML = `This text belongs to rec.autos`;
      } else {
        el("result-label").innerHTML = `${response["result"]}`;
      }
    }
    el("analyze-button").innerHTML = "Analyze";
  };

  var fileData = new FormData();
  fileData.append("input-text", el("input-text").value);
  xhr.send(fileData);
}

