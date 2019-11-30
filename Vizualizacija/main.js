let allYears = [],
mainObj = {};

let showYears = function(){
  for(let key in allYears){
    console.log(allYears[key].key);
    document.getElementById('output').innerHTML = "leto " + allYears[key].key;
  }
}


fetch("data.json")
  .then(function(resp){
    return resp.json();
  })
  .then(function(data){
    mainObj = data.aggregations.uniq_gender;
    allYears = mainObj.buckets;
    showYears();
  });
