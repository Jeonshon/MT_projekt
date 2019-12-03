
//npm install @elastic/elasticsearch to je treba pognat v terminalu da sploh najde modul
//const { Client } = require('@elastic/elasticsearch')
//const client = new Client({ node: 'http://localhost:9200' })

//import * as d3 from "d3";


define(['scripts/d3', 'scripts/elasticsearch'], function (d3, es) {
  //console.log(elasticsearch);
  "use strict";
  var client = new elasticsearch.Client();
  //console.log(client);


  //const { Client } = require(['@elastic/elasticsearch'])
  //const client = new Client({ node: 'http://localhost:9200' })


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


//Vrne seštevek zneska za posamezno polizično kategorijo
client.search({  
  index: 'posebni',
  size: 10000,
  body: {
    aggs: {
      "kategorije": {
        terms: {
          field: "POL_NAME.keyword",
          order: {
            val: "desc"
          },
          size: 50
        },
        aggs: {
          val: {
            sum: {
              field: "Znesek"
            }
          }
        }
      }
    },
    size: 0,
  _source: {
    excludes: []
  },
  stored_fields: [
    "*"
  ],
  script_fields: {},
  docvalue_fields: [],
  query: {
    bool: {
      must: [],
      filter: [
        {
          match_all: {}
        },
        {
          match_phrase: {
            Leto: {
              query: "2015"
            }
          }
        }
      ],
      should: [],
      must_not: []
    }
  }

    

    // aggs: {
    //   "kategorije": {
    //     terms: {
    //         field: "POL_NAME.keyword",
    //     }
    //   }
    // },
    // aggs: {
    //   "sum":{
    //     sum: {field: "Znesek"}
    //   }
    // }
      // End query.
  }
}).then(function (resp) {

  //console.log(resp);
  //console.log(resp.aggregations.kategorije.buckets);

  var sample = resp.aggregations.kategorije.buckets
  console.log(sample)

  const svg = d3.select("#container").append("svg")
  //const svgContainer = d3.select('#container').append("svg");

  const margin = 180;
  const width = 1300 - 2 * margin;
  const height = 700 - 2 * margin;

  const chart = svg.append('g')
    .attr('transform', `translate(${margin}, ${margin})`);

  const xScale = d3.scaleBand()
    .range([0, width])
    .domain(sample.map((s) => s.key))
    .padding(0.4);
  
  const yScale = d3.scaleLinear()
    .range([height, 0])
    .domain([0, sample[0].val.value]);

  // vertical grid lines
  // const makeXLines = () => d3.axisBottom()
  //   .scale(xScale)

  const makeYLines = () => d3.axisLeft()
    .scale(yScale)

  chart.append('g')
    .attr('transform', `translate(0, ${height})`)
    .call(d3.axisBottom(xScale))
    .selectAll("text")
      .style("text-anchor", "end")
      .style("font", "11px times")
      .attr("dx", "-.4em")
      .attr("dy", ".10em")
      .attr("transform", "rotate(-50)");

  chart.append('g')
    .call(d3.axisLeft(yScale));
  
  chart.append('g')
  .attr('class', 'grid')
  .call(makeYLines()
    .tickSize(-width, 0, 0)
    .tickFormat('')
  )

  const barGroups = chart.selectAll()
    .data(sample)
    .enter()
    .append('g')

    barGroups
    .append('rect')
    .attr('class', 'bar')
    .attr('x', (g) => xScale(g.key))
    .attr('y', (g) => yScale(g.val.value))
    .attr('height', (g) => height - yScale(g.val.value))
    .attr('width', xScale.bandwidth())

    .on('mouseenter', function (actual, i) {
      d3.selectAll('.val.value')
        .attr('opacity', 0)


      d3.select(this)
        .transition()
        .duration(300)
        .attr('opacity', 0.6)
        .attr('x', (a) => xScale(a.key) - 5)
        .attr('width', xScale.bandwidth() + 10)

      const y = yScale(actual.val.value)

      chart.append('line')
        .attr('id', 'limit')
        .attr('x1', 0)
        .attr('y1', y)
        .attr('x2', width)
        .attr('y2', y)
      
      chart.append("text")
      .attr('x', xScale(actual.key))
      .attr('y', yScale(actual.val.value) - 10)
      .style("font", "15px times")
      .attr('id', 'limit')
      .text(`${actual.val.value}€`)

    })

    .on('mouseleave', function () {
      d3.selectAll('.val.value')
        .attr('opacity', 1)

      d3.select(this)
        .transition()
        .duration(300)
        .attr('opacity', 1)
        .attr('x', (a) => xScale(a.key))
        .attr('width', xScale.bandwidth())

      chart.selectAll('#limit').remove()
      chart.selectAll('.divergence').remove()
    })


    svg
    .append('text')
    .attr('class', 'label')
    .attr('x', -(height / 2) - margin)
    .attr('y', margin / 2.4)
    .attr('transform', 'rotate(-90)')
    .attr('text-anchor', 'middle')
    .text('Znesek')

  svg.append('text')
    .attr('class', 'title')
    .attr('x', width / 2 + margin)
    .attr('y', 40)
    .attr('text-anchor', 'middle')
    .text('DRŽAVNI PRORAČUN')

  });





// client.search({
  
//   index: 'posebni',
//   size: 10000,
//   body: {
//       // Begin query.
//       query: {
//         match: {
//              "Leto": "2015" 
//         }
//     },
//     aggs: {
//       "leta": {
//         terms: {
//             field: "POL_NAME.keyword",
//         }
//       }
//     }
//       // End query.
//   }
// }).then(function (resp) {
//       console.log("KOKOKOKOKOKO");
//       //var touchdowns = resp.body.hits.hits.aggregations.POL_NAME.buckets;
//       console.log(resp.hits.hits);
//       console.log(resp.aggregations.leta.buckets);
//       console.log(resp.aggregations.leta.buckets.keys);


//       var vrednosti = resp.aggregations.leta.buckets;
//       var sektor = [];
//       var znesek = [];
      

//       for(var i in vrednosti){
//           console.log(vrednosti[i].key);
//           sektor.push(vrednosti[i].key);
//           console.log(vrednosti[i].doc_count);
//           znesek.push(vrednosti[i].doc_count);
  
//       }


//       var margin = {top: 10, right: 30, bottom: 30, left: 40},
//     width = 460 - margin.left - margin.right,
//     height = 400 - margin.top - margin.bottom;
    
//       //console.log(sektor);
//       var svg = d3.select("#donutchart")
//       .append("svg")
//         .attr("width", width + margin.left + margin.right)
//         .attr("height", height + margin.top + margin.bottom)
//       .append("g")
//         .attr("transform",
//               "translate(" + margin.left + "," + margin.top + ")");
    
//     // get the data
//       d = znesek
    
//       // X axis: scale and draw:
//       var x = d3.scaleLinear()
//           .domain(sektor)     // can use this instead of 1000 to have the max of data: d3.max(data, function(d) { return +d.price })
//           .range([0, width]);
//       svg.append("g")
//           .attr("transform", "translate(0," + height + ")")
//           .call(d3.axisBottom(x));


//       // set the parameters for the histogram
//       var histogram = d3.histogram()
//       .value(function(d) { return d; })   // I need to give the vector of value
//       .domain(x.domain())  // then the domain of the graphic
//       .thresholds(x.ticks(70)); // then the numbers of bins





//       //var touchdowns = resp.body.aggregations.leta.buckets
//       var touchdowns = resp.aggregations.leta.buckets
//       // d3 donut chart
//       var width = 600,
//       height = 300,
//       radius = Math.min(width, height) / 2;

//       var color = ['#ff7f0e', '#d62728', '#2ca02c', '#1f77b4'];



//       // var canvas = d3.select("#donut-chart")
//       //   .append("svg:svg")
//       //   .attr("width", '100%')//canvasWidth)
//       //   .attr("height", '100%');//canvasHeight);
});
