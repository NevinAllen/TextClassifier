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
      if (response["result"] == "negative") {
        el("result-label").innerHTML = `That's not nice.`;
        el("result-label").innerHTML = "Rating: " + average ;
      } else if (response["result"] == "neutral") {
        el("result-label").innerHTML = `Okay..`;
        el("result-label").innerHTML = "Rating: " + average ;
      } else if (response["result"] == "positive") {
        el("result-label").innerHTML = `Keep it up!`;
        el("result-label").innerHTML = "Rating: " + average ;
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

