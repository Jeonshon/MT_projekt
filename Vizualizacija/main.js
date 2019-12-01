let allYears = [],
mainObj = {};

let showYears = function(){
  for(let key in allYears){
    //document.getElementById('output').innerHTML += allYears[key].key;

      var butt=document.createElement("button");

      butt.style.backgroundColor = "#4CAF50";
      butt.style.border = "none";
      butt.style.color = "white";
      butt.style.padding = "15px 55px";
      butt.style.textAlign = "center";
      butt.style.display = "inline-block";
      butt.style.marginRight = "30px";
      butt.style.fontSize = "30px";
      butt.style.boxShadow = "0 8px 16px 0 rgba(0,0,0,0.2), 0 6px 20px 0 rgba(0,0,0,0.19)";

      function changeColor(){
        this.style.backgroundColor = "#5d98fb";
        return false;
      }
      
      butt.addEventListener("click", changeColor, false);

      butt.innerHTML = allYears[key].key;                       //dodam v HTML
      document.getElementById("output").appendChild(butt);      //dodam v HTML
      
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
})
