console.log('222222222222222222222222');


const es = require('@elastic/elasticsearch');
const esClient = new es.Client({
    node: 'http://localhost:9200',
    log: 'trace'
});

module.exports = esClient;


// define(['scripts/d3', 'scripts/elasticsearch'], function (d3, es) {
//     "use strict";
    
//     const { Client } = require(['@elastic/elasticsearch'])
//     const client = new Client({ node: 'http://localhost:9200' })
//     async function run () {
//     // Let's search!
//     const { body } = await client.search({
//         index: 'posebni',
//         body: {
//         query: {
//             match: {
//             Leto: '2015'
//             }
//         }
//         }
//     })
//     console.log(body.hits.hits)
//     }
//     run().catch(console.log)
    


//     var client = new elasticsearch.Client({
//         host: 'http://localhost:9200',
//         log: 'trace'
//     });
//     client.search({
//         index: 'posebni',
//         body: {
//             // Begin query.
//             query: {
//                 "size":"0",
//                   "aggs" : {
//                     "poLetih" : {
//                       "terms" : { "field" : "Leto" }
//                   }
//                 }
//               }
//             // Aggregate on the results
//             // End query.
//         }
//     }).then(function (resp) {
//         console.log(resp);
//         // D3 code goes here.
//     });
//});