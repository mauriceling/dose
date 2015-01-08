# -*- coding: utf-8 -*-
# Tkinter canvas to SVG exporter
#
# license: BSD
#
# author: Wojciech Muła
# e-mail: wojciech_mula@poczta.onet.pl
# WWW   : http://0x80.pl/

__author__  = "Wojciech Muła <wojciech_mula@poczta.onet.pl>"

__all__ = ["convert", "SVGdocument", "saveall"]

try:
	# python3
	import tkinter
	from tkinter.constants import *
except ImportError:
	# python2
	import Tkinter as tkinter
	from Tkconstants import *


def warn(msg):
	from sys import stderr

	stderr.write('canvas2svg warning: ')
	stderr.write(msg)
	stderr.write('\n')


def convert(document, canvas, items=None, tounicode=None):
	"""
	Convert 'items' stored in 'canvas' to SVG 'document'.
	If 'items' is None, then all items are convered.

	tounicode is a function that get text and returns
	it's unicode representation. It should be used when
	national characters are used on canvas.

	Return list of XML elements
	"""
	tk = canvas.tk

	if items is None:	# default: all items
		items = canvas.find_all()

	supported_item_types = \
		set(["line", "oval", "polygon", "rectangle", "text", "arc"])
	
	if tounicode is None:
		try:
			# python3
			bytes
			tounicode = lambda x: x
		except NameError:
			# python2
			tounicode  = lambda text: str(text).encode("utf-8")

	elements = []
	for item in items:
		
		# skip unsupported items
		itemtype = canvas.type(item)
		if itemtype not in supported_item_types:
			warn("Items of type '%s' are not supported." % itemtype)
			continue

		# get item coords
		coords = canvas.coords(item)

		# get item options;
		# options is a dict: opt. name -> opt. actual value
		tmp     = canvas.itemconfigure(item)
		options = dict((v0, v4) for v0, v1, v2, v3, v4 in tmp.values())
		
		# get state of item
		state = options['state']
		if 'current' in options['tags']:
			options['state'] = ACTIVE
		elif options['state'] == '':
			options['state'] = 'normal'
		else:
			# left state unchanged
			assert options['state'] in ['normal', DISABLED, 'hidden']


		def get(name, default=""):
			if state == ACTIVE and options.get(state + name):
				return options.get(state + name)
			if state == DISABLED and options.get(state + name):
				return options.get(state + name)

			if options.get(name):
				return options.get(name)
			else:
				return default
		
		
		if itemtype == 'line':
			options['outline'] 			= ''
			options['activeoutline'] 	= ''
			options['disabledoutline'] 	= ''
		elif itemtype == 'arc' and options['style'] == ARC:
			options['fill'] 			= ''
			options['activefill'] 		= ''
			options['disabledfill'] 	= ''

		style = {}
		style["stroke"] = HTMLcolor(canvas, get("outline"))

		if get("fill"):
			style["fill"] = HTMLcolor(canvas, get("fill"))
		else:
			style["fill"] = "none"

		
		width = float(options['width'])
		if state == ACTIVE:
			width = max(float(options['activewidth']), width)
		elif state == DISABLED:
			if float(options['disabledwidth']) > 0:
				width = options['disabledwidth']
	
		if width != 1.0:
			style['stroke-width'] = width
	
		
		if width:
			dash = canvas.itemcget(item, 'dash')
			if state == DISABLED and canvas.itemcget(item, 'disableddash'):
				dash = canvas.itemcget(item, 'disableddash')
			elif state == ACTIVE and canvas.itemcget(item, 'activedash'):
				dash = canvas.itemcget(item, 'activedash')

			if dash != '':
				try:
					dash = tuple(map(int, dash.split()))
				except ValueError:
					# int can't parse literal, dash defined with -.,_
					linewidth = float(get('width'))
					dash = parse_dash(dash, linewidth)

				style['stroke-dasharray']  = ",".join(map(str, dash))
				style['stroke-dashoffset'] = options['dashoffset']


		if itemtype == 'line':
			# in this case, outline is set with fill property
			style["fill"], style["stroke"] = "none", style["fill"]
		
			style['stroke-linecap'] = cap_style[options['capstyle']]

			if options['smooth'] in ['1', 'bezier', 'true']:
				element = smoothline(document, coords)
			elif options['smooth'] == 'raw':
				element = cubic_bezier(document, coords)
			elif options['smooth'] == '0':
				if len(coords) == 4:
					# segment
					element = segment(document, coords)
				else:
					# polyline
					element = polyline(document, coords)
					style['fill'] = "none"
					style['stroke-linejoin'] = join_style[options['joinstyle']]
			else:
				warn("Unknown smooth type: %s. Falling back to smooth=0" % options['smooth'])
				element = polyline(coords)
				style['stroke-linejoin'] = join_style[options['joinstyle']]

			elements.append(element)
			if options['arrow'] in [FIRST, BOTH]:
				arrow = arrow_head(document, coords[2], coords[3], coords[0], coords[1], options['arrowshape'])
				arrow.setAttribute('fill', style['stroke'])
				elements.append(arrow)
			if options['arrow'] in [LAST, BOTH]:
				arrow = arrow_head(document, coords[-4], coords[-3], coords[-2], coords[-1], options['arrowshape'])
				arrow.setAttribute('fill', style['stroke'])
				elements.append(arrow)

		elif itemtype == 'polygon':
			if options['smooth'] in ['1', 'bezier', 'true']:
				element = smoothpolygon(document, coords)
			elif options['smooth'] == '0':
				element = polygon(document, coords)
			else:
				warn("Unknown smooth type: %s. Falling back to smooth=0" % options['smooth'])
				element = polygon(document, coords)

			elements.append(element)

			style['fill-rule'] = 'evenodd'
			style['stroke-linejoin'] = join_style[options['joinstyle']]
		
		elif itemtype == 'oval':
			element = oval(document, coords)
			elements.append(element)

		elif itemtype == 'rectangle':
			element = rectangle(document, coords)
			elements.append(element)

		elif itemtype == 'arc':
			element = arc(document, coords, options['start'], options['extent'], options['style'])
			if options['style'] == ARC:
				style['fill'] = "none"

			elements.append(element)

		elif itemtype == 'text':
			style['stroke'] = '' # no stroke
			
			# setup geometry
			xmin, ymin, xmax, ymax = canvas.bbox(item)
			
			x = coords[0]

			# set y at 'dominant-baseline'
			y = ymin + font_metrics(tk, options['font'], 'ascent') 
			
			element = setattribs(
				document.createElement('text'),
				x = x, y = y 
			)
			elements.append(element)

			element.appendChild(document.createTextNode(
				tounicode(canvas.itemcget(item, 'text'))
			))

			# 2. Setup style
			actual = font_actual(tk, options['font'])

			style['fill'] = HTMLcolor(canvas, get('fill'))
			style["text-anchor"] = text_anchor[options["anchor"]]
			style['font-family'] = actual['family']

			# size
			size = float(actual['size'])
			if size > 0: # size in points
				style['font-size'] = "%spt" % size
			else:        # size in pixels
				style['font-size'] = "%s" % (-size)

			style['font-style']  = font_style[actual['slant']]
			style['font-weight'] = font_weight[actual['weight']]

			# overstrike/underline
			if actual['overstrike'] and actual['underline']:
				style['text-decoration'] = 'underline line-through'
			elif actual['overstrike']:
				style['text-decoration'] = 'line-through'
			elif actual['underline']:
				style['text-decoration'] = 'underline'


		for attr, value in style.items():
			if value: # create only nonempty attributes
				element.setAttribute(attr, str(value))

	return elements


def SVGdocument():
	"Create default SVG document"

	import xml.dom.minidom
	implementation = xml.dom.minidom.getDOMImplementation()
	doctype = implementation.createDocumentType(
		"svg", "-//W3C//DTD SVG 1.1//EN",
		"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd"
	)
	document= implementation.createDocument(None, "svg", doctype)
	document.documentElement.setAttribute(
		'xmlns', 'http://www.w3.org/2000/svg'
	)
	return document


def saveall(filename, canvas, items=None, margin=10, tounicode=None):
	doc = SVGdocument()

	for element in convert(doc, canvas, items, tounicode):
		doc.documentElement.appendChild(element)

	if items is None:
		x1, y1, x2, y2 = canvas.bbox(ALL)
	else:
		x1 = None
		y1 = None
		x2 = None
		y2 = None
		for item in items:
			X1, Y1, X2, Y2 = canvas.bbox(item)
			if x1 is None:
				x1 = X1
				y1 = Y1
				x2 = X2
				y2 = Y2
			else:
				x1 = min(x1, X1)
				x2 = max(x2, X2)
				y1 = min(y1, Y1)
				y2 = max(y2, Y2)
	
	x1 -= margin
	y1 -= margin
	x2 += margin
	y2 += margin

	dx = x2-x1
	dy = y2-y1
	doc.documentElement.setAttribute('width',  "%0.3f" % dx)
	doc.documentElement.setAttribute('height', "%0.3f" % dy)
	doc.documentElement.setAttribute(
		'viewBox', "%0.3f %0.3f %0.3f %0.3f" % (x1, y1, dx, dy))

	file = open(filename, 'w')
	file.write(doc.toxml())
	file.close()


#========================================================================
# canvas elements geometry

def segment(document, coords):
	"polyline with 2 vertices"
	return setattribs(
		document.createElement('line'),
		x1 = coords[0],
		y1 = coords[1],
		x2 = coords[2],
		y2 = coords[3],
	)


def polyline(document, coords):
	"polyline with more then 2 vertices"
	points = []
	for i in range(0, len(coords), 2):
		points.append("%s,%s" % (coords[i], coords[i+1]))
	
	return setattribs(
		document.createElement('polyline'),
		points = ' '.join(points),
	)


def smoothline(document, coords):
	"smoothed polyline"
	element = document.createElement('path')
	path    = []

	points  = [(coords[i], coords[i+1]) for i  in range(0, len(coords), 2)]
	def pt(points):
		x0, y0 = points[0]
		x1, y1 = points[1]
		p0     = (2*x0-x1, 2*y0-y1)

		x0, y0 = points[-1]
		x1, y1 = points[-2]
		pn     = (2*x0-x1, 2*y0-y1)

		p = [p0] + points[1:-1] + [pn]

		for i in range(1, len(points)-1):
			a = p[i-1]
			b = p[i]
			c = p[i+1]

			yield lerp(a, b, 0.5), b, lerp(b, c, 0.5)


	for i, (A, B, C) in enumerate(pt(points)):
		if i == 0:
			path.append("M%s,%s Q%s,%s %s,%s" % (A[0], A[1], B[0], B[1], C[0], C[1]))
		else:
			path.append("T%s,%s" % (C[0], C[1]))

	element.setAttribute('d', ' '.join(path))
	return element

def cubic_bezier(document, coords):
	"cubic bezier polyline"
	element = document.createElement('path')
	points  = [(coords[i], coords[i+1]) for i  in range(0, len(coords), 2)]
	path    = ["M%s %s" %points[0]]
	for n in xrange(1, len(points), 3):
		A, B, C = points[n:n+3]
		path.append("C%s,%s %s,%s %s,%s" % (A[0], A[1], B[0], B[1], C[0], C[1]))
	element.setAttribute('d', ' '.join(path))
	return element


def polygon(document, coords):
	"filled polygon"
	points = []
	for i in range(0, len(coords), 2):
		points.append("%s,%s" % (coords[i], coords[i+1]))

	return setattribs(document.createElement('polygon'),
		points = ' '.join(points)
	)


def smoothpolygon(document, coords):
	"smoothed filled polygon"
	
	element = document.createElement('path')
	path    = []
	points  = [(coords[i], coords[i+1]) for i  in range(0, len(coords), 2)]
	def pt(points):
		p = points
		n = len(points)
		for i in range(0, len(points)):
			a = p[(i-1) % n]
			b = p[i]
			c = p[(i+1) % n]

			yield lerp(a, b, 0.5), b, lerp(b, c, 0.5)
		
	for i, (A, B, C) in enumerate(pt(points)):
		if i == 0:
			path.append("M%s,%s Q%s,%s %s,%s" % (A[0], A[1], B[0], B[1], C[0], C[1]))
		else:
			path.append("T%s,%s" % (C[0], C[1]))
	
	path.append("z")

	element.setAttribute('d', ' '.join(path))
	return element


def rectangle(document, coords):
	element = document.createElement('rect')
	return setattribs(element,
		x = coords[0],
		y = coords[1],
		width  = coords[2]-coords[0],
		height = coords[3]-coords[1],
	)


def oval(document, coords):
	"circle/ellipse"
	x1, y1, x2, y2 = coords

	# circle
	if x2-x1 == y2-y1:
		return setattribs(document.createElement('circle'),
			cx = (x1+x2)/2,
			cy = (y1+y2)/2,
			r  = abs(x2-x1)/2,
		)
	
	# ellipse
	else:
		return setattribs(document.createElement('ellipse'),
			cx = (x1+x2)/2,
			cy = (y1+y2)/2,
			rx = abs(x2-x1)/2,
			ry = abs(y2-y1)/2,
		)
	
	return element


def arc(document, bounding_rect, start, extent, style):
	"arc, pieslice (filled), arc with chord (filled)"
	(x1, y1, x2, y2) = bounding_rect
	import math
	
	cx = (x1 + x2)/2.0
	cy = (y1 + y2)/2.0

	rx = (x2 - x1)/2.0
	ry = (y2 - y1)/2.0
	
	start  = math.radians(float(start))
	extent = math.radians(float(extent))

	# from SVG spec:
	# http://www.w3.org/TR/SVG/implnote.html#ArcImplementationNotes
	x1 =  rx * math.cos(start) + cx
	y1 = -ry * math.sin(start) + cy # XXX: ry is negated here

	x2 =  rx * math.cos(start + extent) + cx
	y2 = -ry * math.sin(start + extent) + cy # XXX: ry is negated here

	if abs(extent) > math.pi:
		fa = 1
	else:
		fa = 0

	if extent > 0.0:
		fs = 0
	else:
		fs = 1
	
	path = []
	# common: arc
	path.append('M%s,%s' % (x1, y1))
	path.append('A%s,%s 0 %d %d %s,%s' % (rx, ry, fa, fs, x2, y2))
	
	if style == ARC:
		pass
	
	elif style == CHORD:
		path.append('z')

	else: # default: pieslice
		path.append('L%s,%s' % (cx, cy))
		path.append('z')

	return setattribs(document.createElement('path'), d = ''.join(path))


#========================================================================
# helpers

def setattribs(element, **kwargs):
	for k, v in kwargs.items():
		element.setAttribute(k, str(v))
	return element


def lerp(vec1, vec2, t):
	(xa, ya) = vec1
	(xb, yb) = vec2
	return (xa + t*(xb-xa), ya + t*(yb-ya))


def HTMLcolor(canvas, color):
	"returns Tk color in form '#rrggbb' or '#rgb'"
	if color:
		# r, g, b \in [0..2**16]

		r, g, b = ["%02x" % (c/256) for c in canvas.winfo_rgb(color)]

		if (r[0] == r[1]) and (g[0] == g[1]) and (b[0] == b[1]):
			# shorter form #rgb
			return "#" + r[0] + g[0] + b[0]
		else:
			return "#" + r + g + b
	else:
		return color


def arrow_head(document, x0, y0, x1, y1, arrowshape):
	"make arrow head at (x1,y1), arrowshape is tuple (d1, d2, d3)"
	import math
	 
	dx = x1 - x0
	dy = y1 - y0

	poly = document.createElement('polygon')
	
	d = math.sqrt(dx*dx + dy*dy)
	if d == 0.0: # XXX: equal, no "close enough"
		return poly

	d1, d2, d3 = list(map(float, arrowshape))
	P0 = (x0, y0)
	P1 = (x1, y1)
	
	xa, ya = lerp(P1, P0, d1/d)
	xb, yb = lerp(P1, P0, d2/d)

	t = d3/d
	xc, yc = dx*t, dy*t

	points = [
		x1, y1,
		xb - yc, yb + xc,
		xa, ya,
		xb + yc, yb - xc,
	]
	poly.setAttribute('points', ' '.join(map(str, points)))
	return poly


def font_actual(tkapp, font):
	"actual font parameters"
	tmp = tkapp.call('font', 'actual', font)
	return dict(
		(tmp[i][1:], tmp[i+1]) for i in range(0, len(tmp), 2)
	)
	
def font_metrics(tkapp, font, property=None):
	if property is None:
		tmp = tkapp.call('font', 'metrics', font)
		return dict(
			(tmp[i][1:], int(tmp[i+1])) for i in range(0, len(tmp), 2)
		)
	else:
		return int(tkapp.call('font', 'metrics', font, '-' + property))


def parse_dash(string, width):
	"parse dash pattern specified with string"
	
	# DashConvert from {tk-sources}/generic/tkCanvUtil.c
	w = max(1, int(width + 0.5))

	n = len(string)
	result = []
	for i, c in enumerate(string):
		if c == " " and len(result):
			result[-1] += w + 1
		elif c == "_":
			result.append(8*w)
			result.append(4*w)
		elif c == "-":
			result.append(6*w)
			result.append(4*w)
		elif c == ",":
			result.append(4*w)
			result.append(4*w)
		elif c == ".":
			result.append(2*w)
			result.append(4*w)
	return result

#========================================================================
# property translation tables

cap_style = {
	"butt"		: "",	# butt: SVG default
	"round"		: "round",
	"projecting": "square",
	""			: "",	# butt: default in Tk & SVG
}

join_style = {
	"bevel"	: "bevel",
	"miter"	: "",		# SVG default
	"round"	: "round"
}

text_anchor = {
	SE	: "end",
	E	: "end",
	NE	: "end",

	SW	: "", # SVG defaul (value "start")
	W	: "",
	NW	: "",

	N	: "middle",
	S	: "middle",
	CENTER: "middle",
}

font_style = {
	"italic"	: "italic",
	"roman"		: "" # SVG default 
}

font_weight = {
	"bold"		: "bold",
	"normal"	: "" # SVG default
}


# vim: ts=4 sw=4 nowrap noexpandtab
