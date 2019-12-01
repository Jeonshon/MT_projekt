'use strict'

//npm install @elastic/elasticsearch to je treba pognat v terminalu da sploh najde modul

const { Client } = require('@elastic/elasticsearch')
const client = new Client({ node: 'http://localhost:9200' })

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
  size: 1,
  body: {
      // Begin query.
      query: {
        match: {
             "Leto": "2015" 
        }
    }
      // End query.
  }
}).then(function (resp) {
      console.log("KOKOKOKOKOKO");
      //var touchdowns = resp.body.hits.hits.aggregations.POL_NAME.buckets;
      console.log(resp.body.hits.hits);
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
