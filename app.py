import os
from flask import Flask
from flask import request
import kulucka
import time
import json
app = Flask(__name__)

@app.route('/ajax',methods = ['POST', 'GET'])
def ajax():
    klc = kulucka.kulucka()
    klc.baglan()
    klc.main()
    k1s = klc.sonuc
    
    print(json.dumps(k1s))
    return json.dumps(k1s)
#lamba yak
@app.route('/ajax2',methods = ['POST', 'GET'])
def ajax2():
    
    klc = kulucka.kulucka()
    klc.port = 503
    klc.baglan()
    
    btn = request.args.get("btn")
    if btn:
        btn = btn.split(",")
        lst = [0,0,0,0]
        for key, val in enumerate(btn):
            if val == "false":
                lst[key] = "0"
            else:
                lst[key] = "1"
        
        value = 0

        for i in range(len(lst)):
            digit = lst.pop()
            if digit == '1':
                value = value + pow(2, i)
        klc.c.write_single_register(0, value)
        time.sleep(.1)
    
    
    
    sonuc = klc.c.read_holding_registers(0, 1)[0]
    klc.c.close()
    #print(sonuc)
    return str(sonuc)
    
@app.route('/testplc' ,methods = ['POST', 'GET'])
def testplc():
    return """<html><head><meta name="viewport" content="width=device-width, initial-scale=1.0">


    

</head>
<style>
.button {color: rgb(230, 230, 230);
font-size: 20px;
padding: 20px;
text-shadow: 0px -1px 0px rgba(30, 30, 30, 0.8);
-webkit-border-radius: 30px;
-moz-border-radius: 30px;
border-radius: 30px;
background: rgb(210, 20, 20);
background: -moz-linear-gradient(90deg, rgb(210, 20, 20) 30%, rgb(250, 20, 20) 70%);
background: -webkit-linear-gradient(90deg, rgb(210, 20, 20) 30%, rgb(250, 20, 20) 70%);
background: -o-linear-gradient(90deg, rgb(210, 20, 20) 30%, rgb(250, 20, 20) 70%);
background: -ms-linear-gradient(90deg, rgb(210, 20, 20) 30%, rgb(250, 20, 20) 70%);
background: linear-gradient(0deg, rgb(210, 20, 20) 30%, rgb(250, 20, 20) 70%);
-webkit-box-shadow: 0px 2px 1px rgba(50, 50, 50, 0.75);
-moz-box-shadow:    0px 2px 1px rgba(50, 50, 50, 0.75);
box-shadow:         0px 2px 1px rgba(50, 50, 50, 0.75);
}
</style>

<body>

<script>


function init(){
    xml = new XMLHttpRequest();
    xml.onreadystatechange= function(){
        if (this.readyState == 4 && this.status == 200){
            res = xml.responseText;
            btn_isle(res);
        }
    };
    xml.open("GET", "/ajax2", true);
    xml.send();
}
function btn_isle(res){
  binary = parseInt(res).toString(2);
  
  for(i in binary){
      
    if(binary[i] == "1"){
        btns[i] = true;
        btnyaz = document.getElementById("btn" + (parseInt(i)+1).toString());
        btnyaz.innerHTML.replace("OFF", "ON");
        btnyaz.setAttribute("style", "background:rgba(0, 0, 0, 0) linear-gradient(0deg, rgb(21, 200, 20) 30%, rgb(25, 200, 20) 70%) repeat scroll 0% 0% / auto padding-box border-box");
        
        
    }
    else{
        btns[i] = false;
        btnyaz = document.getElementById("btn" + (parseInt(i)+1).toString());
        btnyaz.innerHTML.replace("ON", "OFF");
        btnyaz.setAttribute("style", "background:rgba(0, 0, 0, 0) linear-gradient(0deg, rgb(210, 20, 20) 30%, rgb(250, 20, 20) 70%) repeat scroll 0% 0% / auto padding-box border-box");
    }
  }

}
btns = [false, false, false, false];
init();

function renk_yazi(btn){
    btn.innerHTML = (btn.innerHTML.search("OFF") > -1) ? btn.innerHTML.replace("OFF", "ON") :
    btn.innerHTML.replace("ON", "OFF");
    if (btn.innerHTML.search("ON") > -1) {btn.setAttribute("style", "background:rgba(0, 0, 0, 0) linear-gradient(0deg, rgb(210, 20, 20) 30%, rgb(250, 20, 20) 70%) repeat scroll 0% 0% / auto padding-box border-box");}
    else {btn.setAttribute("style", "background:rgba(0, 0, 0, 0) linear-gradient(0deg, rgb(21, 200, 20) 30%, rgb(25, 200, 20) 70%) repeat scroll 0% 0% / auto padding-box border-box");}
}
function yaksondur(btn){
    navigator.vibrate(100);
    //renk_yazi(btn);
    btn_no = btn.innerHTML.split(" ")[1].split(" ")[0];
    if (btns[parseInt(btn_no)-1] == false) {btns[parseInt(btn_no)-1] = true;}
    else {btns[parseInt(btn_no)-1] = false;}
    xml = new XMLHttpRequest();
    xml.onreadystatechange= function(){
        if (this.readyState == 4 && this.status == 200){
            jsn = xml.responseText;
            btn_isle(jsn);
        }
    };
    xml.open("GET", "/ajax2?btn=" + btns.toString(), true);
    xml.send();
    
    
}

</script>
<button id="btn1" onclick = yaksondur(this) class="button">Lamba 1 ON</button>
<button id="btn2" onclick = yaksondur(this) class="button">Lamba 2 ON</button>
<button id="btn3" onclick = yaksondur(this) class="button">Lamba 3 ON</button>
<button id="btn4" onclick = yaksondur(this) class="button">Lamba 4 ON</button>
</body></html>"""
@app.route('/')
def hello():
    return """<html><head><meta name="viewport" content="width=device-width, initial-scale=1.0">


    

</head>
<style>
table.redTable {
  border: 2px solid #A40808;
  background-color: #EEE7DB;
  width: 100%;
  text-align: center;
  border-collapse: collapse;
  margin-left: auto; 
  margin-right: auto;
  margin-top: 25%;
}
table.redTable td, table.redTable th {
  border: 1px solid #AAAAAA;
  padding: 3px 2px;
}
table.redTable tbody td {
  font-size: 13px;
}
table.redTable tr:nth-child(even) {
  background: #F5C8BF;
}
table.redTable thead {
  background: #A40808;
}
table.redTable thead th {
  font-size: 19px;
  font-weight: bold;
  color: #FFFFFF;
  text-align: center;
  border-left: 2px solid #A40808;
}
table.redTable thead th:first-child {
  border-left: none;
}
table.center {
  
}
table.redTable tfoot {
  font-size: 13px;
  font-weight: bold;
  color: #FFFFFF;
  background: #A40808;
}
table.redTable tfoot td {
  font-size: 13px;
}
table.redTable tfoot .links {
  text-align: right;
}
table.redTable tfoot .links a{
  display: inline-block;
  background: #FFFFFF;
  color: #A40808;
  padding: 2px 8px;
  border-radius: 5px;
}

.button {color: rgb(230, 230, 230);
font-size: 20px;
padding: 20px;
text-shadow: 0px -1px 0px rgba(30, 30, 30, 0.8);
-webkit-border-radius: 30px;
-moz-border-radius: 30px;
border-radius: 30px;
background: rgb(210, 20, 20);
background: -moz-linear-gradient(90deg, rgb(210, 20, 20) 30%, rgb(250, 20, 20) 70%);
background: -webkit-linear-gradient(90deg, rgb(210, 20, 20) 30%, rgb(250, 20, 20) 70%);
background: -o-linear-gradient(90deg, rgb(210, 20, 20) 30%, rgb(250, 20, 20) 70%);
background: -ms-linear-gradient(90deg, rgb(210, 20, 20) 30%, rgb(250, 20, 20) 70%);
background: linear-gradient(0deg, rgb(210, 20, 20) 30%, rgb(250, 20, 20) 70%);
-webkit-box-shadow: 0px 2px 1px rgba(50, 50, 50, 0.75);
-moz-box-shadow:    0px 2px 1px rgba(50, 50, 50, 0.75);
box-shadow:         0px 2px 1px rgba(50, 50, 50, 0.75);
}
</style>
<body onload = yenile()>
<table class="redTable">
<thead>
<tr>
<th>&nbsp;</th>
<th>Kulu&ccedil;ka 1</th>
<th>Kulu&ccedil;ka 2</th>
<th>Kulu&ccedil;ka 3</th>
</tr>
</thead>
<tfoot>
<tr>
<td colspan="4">

</td>
</tr>
</tfoot>
<tbody>
<tr>
<td>SICAKLIK</td>
<td id = "k1s">&nbsp;</td>
<td id = "k2s">&nbsp;</td>
<td id = "k3s">&nbsp;</td>
</tr>
<tr>
<td>NEM</td>
<td id = "k1n">&nbsp;</td>
<td id = "k2n">&nbsp;</td>
<td id = "k3n">&nbsp;</td>
</tr>


</tbody>
</table>
<br>
<br>
<script>
function yenile(){
    btn.innerText = "Yenileniyor";
    xml = new XMLHttpRequest();
    xml.onreadystatechange= function(){
        if (this.readyState == 4 && this.status == 200){
            jsn = xml.responseText;
            isle(jsn);
        }
    };
    xml.open("GET", "/ajax", true);
    xml.send();
    
    
}
function isle(jsn){
    btn.innerText = "Yenile";
    eval("jsn=" + jsn);
    document.getElementById("k1s").innerHTML = jsn.kulucka1.sicaklik + "°";
    document.getElementById("k2s").innerHTML = jsn.kulucka2.sicaklik + "°";
    document.getElementById("k3s").innerHTML = jsn.kulucka3.sicaklik + "°";
    document.getElementById("k1n").innerHTML = "%" + jsn.kulucka1.nem;
    document.getElementById("k2n").innerHTML = "%" + jsn.kulucka2.nem;
    document.getElementById("k3n").innerHTML = "%" + jsn.kulucka3.nem;
    if(typeof(t) == "undefined") t = setInterval("yenile()", 15000);
    
    
}
</script>
<button id="btn" onclick = "yenile()" class="button">Yenile</button>
</body></html>"""

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
