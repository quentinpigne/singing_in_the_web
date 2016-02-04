// Nodes colors
var color = d3.scale.ordinal().range(["#357AB7", "#C72C48", "#FCD21C"]);

// Svg and its dimensions
var svg, w, h;

// D3 force
var force;

// Graph nodes and links
var root, nodes, links;

// Prototype to calculate text width
String.prototype.width = function(font) {
	var f = font || '14px Lato', o = $('<div>' + this + '</div>').css({
		'position' : 'absolute',
		'float' : 'left',
		'white-space' : 'nowrap',
		'visibility' : 'hidden',
		'font' : f
	}).appendTo($('body')), w = o.width();

	o.remove();

	return w;
}

// Max name size
var mns = 50;

// Prototype to truncate text
String.prototype.trunc = function() {
	if (this.length <= mns) {
		return this;
	} else {
		return this.substring(0, mns) + '...';
	}
}

function initGraph() {
	// Set svg dimensions
	w = $("#graph").width();
	h = $("#graph").height();
	
	// Append the svg
	svg = d3.select("#graph").append("svg")
		.attr("width", w)
		.attr("height", h)
		.attr("viewBox", "0 0 " + w + " " + h)
		.attr("preserveAspectRatio", "xMidYMid meet");
	
	// Initial nodes and links
	root = {index:0, x:w/2, y:h/2, fixed:true, name:'', type:0};
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
	var link = svg.selectAll(".link");
	var ellipse = svg.selectAll(".ellipse");
	var title = svg.selectAll(".title");
	var image = svg.selectAll(".image");
	link.attr("x1", function(d) { return d.source.x; })
	    .attr("y1", function(d) { return d.source.y; })
	    .attr("x2", function(d) { return d.target.x; })
	    .attr("y2", function(d) { return d.target.y; });

	ellipse.attr("cx", function(d) { return d.x; })
	    .attr("cy", function(d) { return d.y; });

	image.attr("x", function(d) { return d.x - 32;})
		 .attr("y", function(d) { return d.y - 32});
    
	title.attr("x", function(d) { return d.x; })
		.attr("y", function(d) { return d.y; });

	ellipse.each(collide(0.5));
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
	svg.selectAll(".ellipse").remove();
	svg.selectAll(".image").remove();
	svg.selectAll(".title").remove();
	
	var node = svg.selectAll(".node")
		.data(nodes)
		.enter()
		.append("g")
		.attr("class", function(d) {
			if (d.type == 0 || d.type == 1 || d.type == 2) {
				return "ellipse";
			} else {
				return "image";
			}
		});

	// Add ellipses
	svg.selectAll(".ellipse")
		.append("text")
		.attr("class", "title")
		.attr("text-anchor","middle")
		.attr("dy",".4em")
		.text(function(d) { 
			return d.name.trunc();
		});
	
	// Add texts
	svg.selectAll(".ellipse")
		.append("ellipse")
		.attr("class", "ellipse")
		.attr("rx", function(d) {
				var textWidth = d.name.trunc().width();
				return textWidth != 0 ? textWidth / 2 + 10 : 0;
			})
		.attr("ry", 30)
		.style("fill", function(d) { return color(d.type); })
		.call(force.drag);

	// Add images
	var images = svg.selectAll(".image")
		.append("image")
		.attr("class", "image")
	    .attr("xlink:href", function(d) { return d.src; })
	    .attr("width", "64px")
	    .attr("height", "64px")
	    .call(force.drag);
	
	// Add listener to ellipses
	svg.selectAll(".ellipse").on("click", function(d) {
		if (d3.event.defaultPrevented) return; // ignore drag
		detailNode(d);
	});

	// Make the image grow a little and show some details on mouse over
	var setEvents = images
		.on( 'mouseenter', function() {
			d3.select("h1").html(root.name);
			d3.select("h2").html(root.info);
			// select element in current context
			d3.select( this )
			.transition()
			.attr("x", function(d) { return d.x-64;})
			.attr("y", function(d) { return d.y-64;})
			.attr("height", 128)
			.attr("width", 128);
		})
		// set back
		.on( 'mouseleave', function() {
			d3.select("h1").html("");
			d3.select("h2").html("");
			d3.select( this )
			.transition()
			.attr("x", function(d) { return d.x-32;})
			.attr("y", function(d) { return d.y-32;})
			.attr("height", 64)
			.attr("width", 64);
		});

	startGraph();
}

function updateLinks() {
	svg.selectAll(".link").remove();
	var link = svg.selectAll(".line")
		.data(links)
		.enter()
		.append("line")
		.attr("class", "link");
}

function detailNode(d) {
	// Hide search bar
	$("#search-bar").hide();

	// Node d becomes root
	root.id = d.id;
	root.type = d.type;
	root.name = d.name;

	// Search for node details and relatives
	var detailsRequest = "songs/",
		relativesRequest = "songs/";

	switch(d.type) {
		case 0:
			// Artist node
			detailsRequest += "artist_details/?artist_id=" + root.id;
			relativesRequest += "artist_relatives/?artist_id=" + root.id;
			break;
		case 1:
			// Album node
			detailsRequest += "album_details/?album_id=" + root.id;
			relativesRequest += "album_relatives/?album_id=" + root.id;
			break;
		case 2:
			// Song node
			detailsRequest += "song_details/?song_id=" + root.id;
			relativesRequest += "song_relatives/?song_id=" + root.id;
			break;
	}

	// Details request
	d3.json(detailsRequest)
		.header("Content-Type", "application/x-www-form-urlencoded")
		.get(function(error, data) {
			// Add the details to the root node
			switch(root.type) {
				case 0:
					// Artist node
					root.artist_thumbnail = data.artist_thumbnail;
					root.info = data.artist_location;
					break;
				case 1:
					// Album node
					root.album_cover = data.album_cover;
					root.info = data.album_year;
					break;
				case 2:
					// Song node
					root.song_hotness = data.song_hotness;
					root.analysis_sample_rate = data.analysis_sample_rate;
					root.audio_md5 = data.audio_md5;
					root.danceability = data.danceability;
					root.duration = data.duration;
					root.end_of_fade_in = data.end_of_fade_in;
					root.energy = data.energy;
					root.key_item = data.key_item;
					root.key_confidence = data.key_confidence;
					root.loudness = data.loudness;
					root.mode = data.mode;
					root.mode_confidence = data.mode_confidence;
					root.start_of_fade_out = data.start_of_fade_out;
					root.tempo = data.tempo;
					root.time_signature = data.time_signature;
					root.time_signature_confidence = data.time_signature_confidence;
					break;
			}

			// Relatives request
			d3.json(relativesRequest)
				.header("Content-Type", "application/x-www-form-urlencoded")
				.get(function(error, data) {
					clearNodes();
					// Add all relatives nodes
					$.each(data.nodes, function (index, node) {
						addNode(node);
					});

					// Develop root node details
					switch (root.type) {
						case 0:
							detailArtistNode();
							break;
						case 1:
							detailAlbumNode();
							break;
						case 2:
							break;
					}
					updateLinks();
					updateNodes();
				});
		});
}

function detailArtistNode() {
	// Add an artist thumbnail link from the root node
	var node = {src:root.artist_thumbnail, type:3};
	addNode(node);
}

function detailAlbumNode() {
	// Add an album cover link from the root node
	var node = {src:root.album_cover, type:3};
	addNode(node);
}

function clearNodes() {
	links.splice(0, links.length);
	nodes.splice(1, nodes.length - 1);
}

function addNode(node) {
	nodes.push(node);
	
	// Add a link from the root node
	var link = {source:root, target:node};
	links.push(link);
}

// Search
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

$("#search-input").keyup(searchNodes);

// Responsive
function resize() {
	w = $("#graph").width();
	h = $("#graph").height();
	svg.attr("width", w).attr("height", h);
	force.size([w, h]).resume();
}

d3.select(window).on("resize", resize);

// Init graph
initGraph();