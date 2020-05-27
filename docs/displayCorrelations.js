var myLabel = []
var myDict = {}
var myChart = ""
var pageTopic = ""

function buildChart(aLabel, aDict, title){
  try{
    myChart.destroy();
  }
  catch{

  }
  myChart = new Chart(document.getElementById("line-chart"), {
  type: 'line',
  data: {
    labels: aLabel,
    datasets: aDict
  },
  options: {
    title: {
      display: true,
      text: title
    }
  }
});

selectHTML = "<select id = 'correlationSelectOption'  onchange='changeChart()'>"
for (var pub in myDict){
  selectHTML += "<option value=" + pub + ">" + pub + "</option>"
}
selectHTML += "</select>"

document.getElementById("selectBox").innerHTML = selectHTML
}

function changeChart(){
  try{
    myChart.destroy();
  } catch{

  }
  console.log("HERE")
  var publisher = document.getElementById("correlationSelectOption").value;
  console.log(publisher)
  myChart = new Chart(document.getElementById("line-chart"), {
  type: 'line',
  data: {
    labels: myLabel,
    datasets: convertToChartData(myDict[publisher])
  },
  options: {
    title: {
      display: true,
      text: "topic " + pageTopic +": lagged correlations for "+ publisher
    }
  }
});
}

function addRow(row){
  if(row["source"] != null){
    try{
      var src = row["source"].split("_")
      lag = src[0]
      pub = src[1]
      if (!(myLabel.includes(lag))){
        myLabel.push(lag)
      }
      else{
      }

      for (var key in row){
        if (key != "source"){
          if (key in myDict){

          }
          else{
            myDict[key] = {}
          }

          if (!(pub in myDict[key])){
            myDict[key][pub] = []
          }
          else{

          }
          myDict[key][pub].push(row[key]);
        }
      }

    }
    catch{

    }
  }
};

function randomColor(){
   r = Math.floor(Math.random() * 255)
   g = Math.floor(Math.random() * 255)
   b = Math.floor(Math.random() * 255)
   return "rgb(" + r + "," + g + "," + b + ")"
};


function convertToChartData(someDict){
  console.log(someDict)
  var datasets = []
  for (publisher in someDict){
    newEntry = {}
    newEntry["label"] = publisher
    newEntry["data"] = someDict[publisher]
    newEntry["fill"]=false
    newEntry["borderColor"] =randomColor()
    datasets.push(newEntry)
  }
  return datasets
}

function genGraph(model="american"){
  console.log("https://raw.githubusercontent.com/brockmanmatt/CoverageTrends/master/docs/models/corr/" + model + ".csv")
  Papa.parse("https://raw.githubusercontent.com/brockmanmatt/CoverageTrends/master/docs/models/corr/" + model + ".csv", {
  	download: true,
    dynamicTyping: true,
    header:true,

    complete: function(results) {
      for (row of results["data"]){
  		    addRow(row)
    }
    var getMe = ""
    for (var pub in myDict){
      getMe = pub
      break
    }
    buildChart(myLabel, convertToChartData(myDict[getMe]), "topic " +model+": lagged correlations for "+getMe)
    pageTopic = model
    myChart.canvas.parentNode.style.height = '70%';
    myChart.canvas.parentNode.style.width = '70%';
    myChart.canvas.parentNode.style.maxWidth = '700px';

    }
  });
}
