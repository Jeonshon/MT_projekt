export default function define(runtime, observer) {
  const main = runtime.module();
  main.variable(observer()).define(["md"], function(md){return(
md`# STATE BUDGET

Click to zoom in or out.`
)});
  main.variable(observer("chart")).define("chart", ["pack","data","d3","DOM","width","height"], function(pack,data,d3,DOM,width,height)
{
  const root = pack(data);
  console.log(root)
  let focus = root;
  let view;

  const svg = d3.select(DOM.svg(width, height))
      .attr("viewBox", `-${width / 2} -${height / 2} ${width} ${height}`)
      .style("display", "block")
      .style("margin", "0 -14px")
      .style("width", "calc(100% + 28px)")
      .style("height", "800")
      .style("background", "transparent")
      .style("cursor", "pointer")
      .on("click", () => zoom(root));
var defs = svg.append("defs");

var gradient = defs.append("linearGradient")
   .attr("id", "svgGradient")
   .attr("x1", "0%")
   .attr("x2", "100%")
   .attr("y1", "0%")
   .attr("y2", "100%");

gradient.append("stop")
   .attr('class', 'end')
   .attr("offset", "100%")
   .attr("stop-color", "blue")
   .attr("stop-opacity", 0.3);

gradient.append("stop")
   .attr('class', 'end')
   .attr("offset", "50%")
   .attr("stop-color", "red")
   .attr("stop-opacity", 1);
  
  const node = svg.append("g")
    .selectAll("circle")
    .data(root.descendants().slice(1).map((x)=>{console.log(x);return x;})
          .sort((a, b) => (b.depth- a.depth) || (b.value - a.value)))
    .enter().append("circle")
      .attr("fill", d => "url(#svgGradient)" )
      .style("fill-opacity", d => d.parent === root ? 0.5: 1 )
      .attr("pointer-events", d => !d.children ? "none" : null)
      .on("mouseover", function() { d3.select(this).attr("stroke", "#000"); })
      .on("mouseout", function() { d3.select(this).attr("stroke", null); })
      .on("click", d => focus !== d && (zoom(d), d3.event.stopPropagation()));

  const label = svg.append("g")
      .style("font", "10px sans-serif")
      .attr("pointer-events", "none")
      .attr("text-anchor", "middle")
      .selectAll("text")
      .data(root.descendants())
      .enter().append("text")
      .style("fill-opacity", d => d.parent === root ? 1 : 0)
      .style("display", d => d.parent === root ? "none" : "none")
      .text(d => d.data.name);

  zoomTo([root.x, root.y, root.r * 2]);

  function zoomTo(v) {
    const k = width / v[2];

    view = v;

    label.attr("transform", d => `translate(${(d.x - v[0]) * k},${(d.y - v[1]) * k})`);
    node.attr("transform", d => `translate(${(d.x - v[0]) * k},${(d.y - v[1]) * k})`);
    node.attr("r", d => d.r * k);
  }

  function zoom(d) {
    const focus0 = focus;

    focus = d;

    const transition = svg.transition()
        .duration(d3.event.altKey ? 7500 : 750)
        .tween("zoom", d => {
          const i = d3.interpolateZoom(view, [focus.x, focus.y, focus.r * 2]);
          return t => zoomTo(i(t));
        });
     node
      .filter(function(d) { return d.parent === focus || d===focus})// this.style.display === "inline"; })
      .transition(transition)
        .style("fill-opacity", d => d.parent === focus ? 1 : 0)
        .on("start", function(d) { if (d.parent === focus) this.style.display = "inline"; })
        .on("end", function(d) { if (d.parent !== focus) this.style.display = "none"; });

    label
      .filter(function(d) { return d.parent === focus || this.style.display === "none"; })
      .transition(transition)
        .style("fill-opacity", d => d.parent === focus ? 1 : 0)
        .on("start", function(d) { if (d.parent === focus) this.style.display = "none"; })
        .on("end", function(d) { if (d.parent !== focus) this.style.display = "none"; });
  }

  return svg.node();
}
);
  main.variable(observer("data")).define("data", ["require"], function(require){return(
require("@observablehq/flare")
)});
  main.variable(observer("pack")).define("pack", ["d3","width","height"], function(d3,width,height){return(
data => d3.pack()
    .size([width, height])
    .padding(3)
  (d3.hierarchy(data)
    .sum(d => {
    console.log("dddd",d)
    return d.size
  })
    .sort((a, b) => (a.depth- b.depth) || (b.value - a.value)))
)});
  main.variable(observer("width")).define("width", function(){return(
850
)});
  main.variable(observer("height")).define("height", ["width"], function(width){return(
width
)});
  main.variable(observer("format")).define("format", ["d3"], function(d3){return(
d3.format(",d")
)});
  main.variable(observer("color")).define("color", ["d3"], function(d3){return(
d3.scaleLinear()
    .domain([0, 5])
    .range(["hsl(152,80%,80%)", "hsl(228,30%,40%)"])
    .interpolate(d3.interpolateHcl)
)});
  main.variable(observer("d3")).define("d3", ["require"], function(require){return(
require("d3@5")
)});
  return main;
}
