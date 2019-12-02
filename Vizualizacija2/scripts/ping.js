
//npm install @elastic/elasticsearch to je treba pognat v terminalu da sploh najde modul
// const { Client } = require('@elastic/elasticsearch')
// const client = new Client({ node: 'http://localhost:9200' })




define(['scripts/d3', 'scripts/elasticsearch'], function (d3, es) {
  console.log(elasticsearch);
  "use strict";
  var client = new elasticsearch.Client();
  console.log(client);



// async function run () {
//   // here we are forcing an index refresh, otherwise we will not
//   // get any result in the consequent search
//   await client.indices.refresh({ index: 'posebni' })

//   // Let's search!
//   const result = await client.search({
//     index: 'posebni',
//     // type: '_doc', // uncomment this line if you are using Elasticsearch ≤ 6
//     size: 1000000,
//     body: {
//         query: {
//             match: {
//                  "Leto": "2015" 
//             }
//         }
//     }
//   })
//   console.log(result.body.hits.hits)
// }

// run().catch(console.log)
console.log("test");

client.search({
  
  index: 'posebni',
  size: 10000,
  body: {
      // Begin query.
      query: {
        match: {
             "Leto": "2015" 
        }
    },
    aggs: {
      "leta": {
        terms: {
            field: "POL_NAME.keyword",
        }
      }
    }
      // End query.
  }
}).then(function (resp) {
      console.log("KOKOKOKOKOKO");
      //var touchdowns = resp.body.hits.hits.aggregations.POL_NAME.buckets;
      console.log(resp.hits.hits);
      console.log(resp.aggregations.leta.buckets);
      //var touchdowns = resp.body.aggregations.leta.buckets
      var touchdowns = resp.aggregations.leta.buckets
      // d3 donut chart
      var width = 600,
      height = 300,
      radius = Math.min(width, height) / 2;

      var color = ['#ff7f0e', '#d62728', '#2ca02c', '#1f77b4'];

      var arc = d3.svg.arc()
          .outerRadius(radius - 60)
          .innerRadius(120);

      var pie = d3.layout.pie()
          .sort(null)
          .value(function (d) { return d.doc_count; });

      var svg = d3.select("#donut-chart").append("svg")
          .attr("width", width)
          .attr("height", height)
          .append("g")
          .attr("transform", "translate(" + width/1.4 + "," + height/2 + ")");

      var g = svg.selectAll(".arc")
          .data(pie(touchdowns))
          .enter()
          .append("g")
          .attr("class", "arc");

      g.append("path")
          .attr("d", arc)
          .style("fill", function (d, i) {
              return color[i];
          });

      g.append("text")
          .attr("transform", function (d) { return "translate(" + arc.centroid(d) + ")"; })
          .attr("dy", ".35em")
          .style("text-anchor", "middle")
          .style("fill", "white")
          .text(function (d) { return d.data.key; });
});


// const esClient = require('./main');

// esClient.ping({
// // ping usually has a 3000ms timeout
//     requestTimeout: Infinity
// }, function (error) {
//     if (error) {
//         console.trace('elasticsearch cluster is down!');
//     } else {
//         console.log('All is well');
//     }
// });
});
