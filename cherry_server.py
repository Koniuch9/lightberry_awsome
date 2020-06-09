import cherrypy
import os

class HelloWorld(object):
	@cherrypy.expose
	def index(self):
		os.system("sudo service captureVideo stop")
		os.system("sudo service hyperion stop")
		os.chdir("/home/pi/images2")
		os.system("hyperion-v4l2 --pixel-format YUYV --screenshot --device /dev/video2")
		os.chdir("/home/pi")
		return """
<html>
<head>
<script type="text/javascript">
	var enlarged = false;
	var t = 0;
	var b = 320;
	var l = 0;
	var r = 480;
	var str = "";

	function topUp() {t++;setClip();}
	function topDown() {t--;setClip();}
	function bottomUp() {b++;setClip();}
	function bottomDown() {b--;setClip();}
	function leftUp() {l++;setClip();}
	function leftDown() {l--;setClip();}
	function rightUp() {r++;setClip();}
	function rightDown() {r--;setClip();}

	function setClip() {
		document.getElementById("t").value = t;
		document.getElementById("b").value = b;
		document.getElementById("l").value = l;
		document.getElementById("r").value = r;
		str = "rect("+t+"px "+r+"px "+b+"px "+l+"px)";
		document.getElementById("test").innerHTML = str;
		document.getElementById("screen").style.clip = str;
	}

	function slideR(v) {
		r = v;
		setClip();
	}
function slideT(v) {
		t = v;
		setClip();
	}
function slideL(v) {
		l = v;
		setClip();
	}
function slideB(v) {
		b = v;
		setClip();
	}

window.onscroll = function() {
	window.scrollTo(0,0);
}
</script>
</head>
<style>
	img {
		margin-left:80px;
		position:absolute;
		width:480px
	}
	button {
		width:12%;
		height:auto;
	}
</style>
<body>
<div style="position:absolute" onscroll="onskrol()">
<img id="screen" src="/images2/screenshot.png" width="480px" height="320px"/>
<input type="range" style="position:absolute;top:325px;left:350px;width:200px" min="280" max="480" value="480" id="range" oninput="slideR(this.value)" onchange="slideR(this.value)" />
<input type="range" style="position:absolute;top:325px;left:90px;width:200px" min="0" max="200" value="0" id="range" onchange="slideL(this.value)" oninput="slideL(this.value)" />
<input type="range" style="touch-action:none;position:absolute;top:50px;width:100px;transform:rotate(90deg);" min="0" max="100" value="0" id="range" onchange="slideT(this.value)" oninput="slideT(this.value)" />
<input type="range" style="touch-action:none;position:absolute;top:250px;width:100px;transform:rotate(90deg);" min="220" max="320" value="320" id="range" onchange="slideB(this.value)" oninput="slideB(this.value)" />
</div>
<div style="position:relative;top:360px">
<div style="margin:50px">
<button onclick="topUp()">GORA+</button>
<button onclick="topDown()">GORA-</button>
<button onclick="leftUp()">LEWO+</button>
<button onclick="leftDown()">LEWO-</button>
<button onclick="rightUp()">PRAWO+</button>
<button onclick="rightDown()">PRAWO-</button>
<button onclick="bottomUp()">DOL+</button>
<button onclick="bottomDown()">DOL-</button>
</div>

<p id="test" >SIEMA TEST</p><br/>
<form action="hello" method="post">
	<input id="t" type="hidden" name="top" />
	<input id="r" type="hidden" name="right" />
	<input id="b" type="hidden" name="bottom" />
	<input id="l" type="hidden" name="left" />
	<input style="width:100px;height:100px;color:red" type="submit" name="submit" />
</form><br/><br/>
<form action="restart" method="post" style="margin-top:50px">
	<button name="submit2">RESTART</input>
</form>
</div>




</body>
</html>

"""

	@cherrypy.expose
	def hello(self, submit, top, left, right, bottom):
		os.system("python changeConfig.py " + top + " " + left + " " + bottom + " " + right)
		os.system("sudo service captureVideo start")
		return "top: " + str(top) + ",left: " + str(left) +", right: " + str(right) +",bottom: " + str(bottom)

	@cherrypy.expose
	def restart(self, submit2):
		os.system("sudo service captureVideo start")
		return "<h1>Restarted</h1>"

if __name__ == '__main__':
	cherrypy.config.update({'server.socket_host' : '192.168.0.103',
		'server.socket_port' : 8080})
	conf = {'/images2' : {'tools.staticdir.on' : True,
		'tools.staticdir.dir' : '/home/pi/images2'}}
	cherrypy.quickstart(HelloWorld(), '/', config = conf)
