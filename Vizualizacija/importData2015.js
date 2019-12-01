var vrednosti = [];
var sektor = [];
var znesek = [];

let showSektor = function(){
    for(var i in vrednosti){
        //console.log(vrednosti[i].key);
        sektor.push(vrednosti[i].key);
        //console.log(vrednosti[i].value);
        znesek.push(vrednosti[i].value);

    }
    //console.log(sektor);
}

fetch("SestevekSektorjev2015.json")
  .then(function(resp){
    return resp.json();
  })
  .then(function(data){
    vrednosti = data.aggregations.buckets;
    //console.log(vrednosti);
    showSektor();
})

