from flask import Flask, request
chat = Flask(__name__, static_url_path="", static_folder="static")
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
chat.config['DEBUG'] = True
import re

html = """
<html><head>
<link href="https://fonts.googleapis.com/css?family=Roboto" rel="stylesheet">
<link rel="stylesheet" type="text/css" href="https://csshake.surge.sh/csshake.min.css"> 
<style>
#mychat{width:100%; font-size: 15px; padding: 10px; border: 1px solid #111111;}
</style>
<style>
#chat{height:500px; word-wrap:break-word; overflow: scroll;}
</style>
<style>
body{font-family: 'Roboto', sans-serif;}
</style>
</head><body>
	<script src="https://cdn.jsdelivr.net/npm/js-cookie@2/src/js.cookie.min.js"></script>
	<script src="https://cdn.jsdelivr.net/npm/jdenticon@2.1.0" async></script>
	<script>
	if (Cookies.get('totalmsg') == null) {
		Cookies.set('totalmsg', 0)
	}
	</script>
	<h1>MagnaTalk</h1>
	<div class="totalmsge">0</div> messages envoyé par vous
	<input id="mychat" placeholder="Type message and press enter"/>
	<div id="chat"></div>
	<br>
	<div class="tempidenti"></div>
	<script src="http://code.jquery.com/jquery-1.11.0.min.js"></script>
	<script src="https://cdnjs.cloudflare.com/ajax/libs/underscore.js/1.9.1/underscore-min.js"></script>
	<script>
	$("div.totalmsge").replaceWith('<div class=\"totalmsge\">' + Cookies.get('totalmsg') + '</div>')
	</script>
	<script>
	var username = prompt("Enter your name | Entrez votre nom")
	username = _.escape(username)
	$( "div.tempidenti" ).replaceWith( "<svg data-jdenticon-value='" + username + "' width='80' height='80'>ERREUR Votre Navigateur ne supporte pas les SVG.</svg>" );
	</script>
	<script>
	var grosmots = ['connard', 'C0NNAR', 'pute', 'merde', 'enkuler', 'enculer']
	$('#mychat').keypress(function(e){
		if( e.keyCode==13 ){
			if (grosmots.indexOf($('#mychat').val()) >= 0) {
				alert("Gros mot détecté, veuillez ne pas écrire de gros mots");
				return;
			} else if ($('#mychat').val() == "" || $('#mychat').val() == null) {
				alert("Veuillez ne pas envoyer de messages vides")
			} else {
				$.get('/send',{msg:_.escape($('#mychat').val()), usernem:username});
				$('#mychat').val('');
				var totalmsgb = Number(Cookies.get('totalmsg'))
				totalmsgb = totalmsgb + 1
				Cookies.set('totalmsg', totalmsgb);
				$("div.totalmsge").replaceWith('<div class=\"totalmsge\">' + Cookies.get('totalmsg') + '</div>')
			}
		}
	});
	last = 0;
	setInterval(function(){
		$.get('/update',{last:last},
			function(response){
				last = $('<p>').html(response).find('span').data('last');
				$('#chat').append(response);
				$('span:not(:last)').remove();
				var objDiv = document.getElementById("chat");
				objDiv.scrollTop = objDiv.scrollHeight;
				});
		},1000);
	</script>
</body></html>
"""

msgs = []

@chat.route('/')
def index():return html

@chat.route('/send')
def send():
	flmsg = request.args['msg']
	flmsg = flmsg.replace("NON", "<b>NON</b>")
	flmsg = flmsg.replace("PUTAIN DE MERDE", "<div class='shake shake-constant'>PUTAIN DE MERDE</div>")
	flmsg = flmsg.replace("TRIGGERED", "<div class='shake-crazy shake-constant'><font color='red'><b>TRIGGERED</b></font></div>")
	flmsg = flmsg.replace("PogChamp", "<img src='https://static-cdn.jtvnw.net/emoticons/v1/88/1.0'>")
	flmsg = flmsg.replace("PogCrazy", "<div class='shake shake-constant'><img src='https://static-cdn.jtvnw.net/emoticons/v1/88/1.0'></div>")
	flmsg = flmsg.replace("SP33Dboi", "<img src='/speedboi.png'>")
	#msgs.append('%s:%s' % (request.remote_addr, request.args['msg']))
	msgs.append('<b>%s</b> : %s' % (request.args['usernem'], flmsg))
	print(request.remote_addr + " | " + request.args['usernem'] + " : " + request.args['msg'])
	return ""

@chat.route('/update')
def update():
	updates= msgs[int(request.args['last'])::]
	last = "<span data-last='%s'></span>" % len(msgs)
	if len(updates) > 0:
		return "<br>".join(updates) + last + "<br>"
	else:
		return last

if __name__ == '__main__': chat.run(port=25565)