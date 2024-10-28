
function data_mapper(ID,transcript)
{
    url='/data_mapping?id='+ID+'&data='+transcript;
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
            alert("Prem");
            var data=eval(xhttp.responseText);

            var str=''; // variable to store the options
            for (var i=0; i < data.length;++i){
                str += '<option value="'+data[i]+'" />'; // Storing options in variable
            }
            var my_list=document.getElementById(ID+"_l");
            var demoInput = document.getElementById(ID);
            demoInput.value =transcript; // set default value instead of html attribute
            demoInput.onfocus = function() { demoInput.value =''; }; // on focus - clear input
            demoInput.onblur = function() { demoInput.value =transcript; };
            my_list.innerHTML = str;

    }
    };
    xhttp.open("GET", url, true);
    xhttp.send();
    
};
  
    
function runSpeechRecognition(ID) {
  // get output div reference
  var output = document.getElementById(ID);
  // get action element reference
      // new speech recognition object
      var SpeechRecognition = SpeechRecognition || webkitSpeechRecognition;
      var recognition = new SpeechRecognition();
  
      // This runs when the speech recognition service starts
      recognition.onstart = function (){
        var x = document.getElementById("snackbar");
        x.className = "show";
        setTimeout(function(){ x.className = x.className.replace("show", ""); }, 3000);
      };
      
      
    
      // This runs when the speech recognition service returns result
      recognition.onresult = function(event) {
          var transcript = event.results[0][0].transcript;
          var confidence = event.results[0][0].confidence;
          alert(transcript);
          if(transcript=="mail"){
            transcript="male"
          }
          if(ID!='gender'){
            data_mapper(ID,transcript);
          }
          else{
            output.value=transcript;
          }
          
      };
    
        // start recognition
        recognition.start();
        
};



