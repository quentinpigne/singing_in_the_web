// Nodes colors
var color = d3.scale.ordinal().range(["#357AB7", "#C72C48", "#FCD21C"]);

// Svg and its dimensions
var svg, w, h;

// D3 force
var force;

// Graph nodes and links
var root, nodes, links;

// Root node dimensions
var rw, rh;

// Max name size
var mns = 50;

function initGraph() {
	// Set svg dimensions
	w = $("#graph").width();
	h = $("#graph").height();
	
	// Append the svg
	svg = d3.select("#graph").append("svg")
	    .attr("width", w)
	    .attr("height", h);

	// Set central node dimensions
	rw = w/3;
	rh = 30;
	
	// Initial nodes and links
	root = {index:0, x:w/2, y:h/2, fixed:true, name:'', type:9};
	nodes = [root];
	links = [];
	
	force = d3.layout.force()
		.nodes(nodes)
		.links(links)
		.size([w, h])
		.linkDistance(w/4);
	
	startGraph();
}

function startGraph() {
	force.on("tick", tick)
		.start();
}

function tick() {
	var link = svg.selectAll(".link").data(links);
	var node = svg.selectAll(".node").data(nodes);
	var title = svg.selectAll(".title").data(nodes);
	link.attr("x1", function(d) { return d.source.x; })
	    .attr("y1", function(d) { return d.source.y; })
	    .attr("x2", function(d) { return d.target.x; })
	    .attr("y2", function(d) { return d.target.y; });
	
	node.attr("cx", function(d) { return d.x; })
	    .attr("cy", function(d) { return d.y; });
    
	title.attr("x", function(d) { return d.x; })
		.attr("y", function(d) { return d.y; });
	node.each(collide(0.5));
}

// Gestion des collisions

var padding = 1;

function collide(alpha) {
	var quadtree = d3.geom.quadtree(nodes);
	return function(d) {
		quadtree.visit(function(quad, x1, y1, x2, y2) {
			var rb = Math.min(d.name.length*8, mns*4) + padding;
			var nx1 = d.x - rb;
			var nx2 = d.x + rb;
			var ny1 = d.y - rb;
			var ny2 = d.y + rb;
			if (quad.point && (quad.point !== d)) {
				var x = d.x - quad.point.x;
				var y = d.y - quad.point.y;
				l = Math.sqrt(x * x + y * y);
				if (l < rb) {
					l = (l - rb) / l * alpha;
					d.x -= x *= l;
					d.y -= y *= l;
					quad.point.x += x;
					quad.point.y += y;
				}
			}
			return x1 > nx2 || x2 < nx1 || y1 > ny2 || y2 < ny1;
		});
	};
}

// Fin de gestion des collisions

function updateNodes() {
	svg.selectAll(".link").remove();
	svg.selectAll(".node").remove();
	svg.selectAll(".title").remove();
	
	// Customize links and nodes
	var link = svg.selectAll(".link")
		.data(links)
		.enter().append("line");
	var title = svg.selectAll(".title")
		.data(nodes)
		.enter()
		.append("text")
		.attr("class", "title")
		.attr("text-anchor","middle")
		.attr("dy",".4em")
		.text(function(d) { 
			if (d.name.length <= mns) {
				return d.name; 
			} else {
				return d.name.substring(0, mns) + '...';
			}
		});
	
	var node = svg.selectAll(".node")
		.data(nodes)
		.enter().append("ellipse")
		.attr("class", "node")
		.attr("rx", function(d) { return Math.min(d.name.length * 4, mns*4); })
		.attr("ry", 30)
		.style("fill", function(d) { return color(d.type); })
		.call(force.drag);
	
	startGraph();
}

function clearNodes() {
	nodes.splice(1, nodes.length - 1);
	links.splice(0, links.length);
}

function addNode(node) {
	nodes.push(node);
	
	// Add a link from the root node
	var link = {source:root, target:node};
	links.push(link);
}

function searchNodes() {
	var query = $("#search-input").val();
	d3.json("songs/search/?query=" + encodeURI(query))
		.header("Content-Type", "application/x-www-form-urlencoded")
		.get(function(error, data) {
			clearNodes();
			$.each(data.nodes, function (index, node) {
				addNode(node);
			});
		updateNodes();
	});
}

function resize() {
	var width = $("#graph").width();
	var height = $("#graph").height();
	svg.attr("width", width).attr("height", height);
	force.size([force.size()[0]+(width-w),force.size()[1]+(height-h)]).resume();
    w = width;
	h = height;
}

d3.select(window).on("resize", resize);

$("#search-input").keyup(searchNodes);

// Init graph
initGraph();


