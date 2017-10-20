var apiKey,
    sessionId,
    token,
    accountType,
    ffWhitelistVersion;

$(document).ready(function() {
  // See the confing.js file.
  if (API_KEY && TOKEN && SESSION_ID) {
    apiKey = API_KEY;
    sessionId = SESSION_ID;
    token = TOKEN;
    accountType = ACCOUNT_TYPE;
   
    if(accountType == 'teacher'){
	if(chrome && chrome.runtime && chrome.runtime.sendMessage) {
  		chrome.runtime.sendMessage(
    			"faidodiononpbbplbjppmandaplonida",
    			{type: "isInstalled"},
    			function(response) {
				console.log(response);
				if(response){
					initializeSession2();
				} else {
					document.getElementById("installModal").style.display = 'block';
				}
			}
  		);
}
    } else {
	initializeSession2();
    }
  }
});


function installApp(){
	chrome.webstore.install('https://chrome.google.com/webstore/detail/faidodiononpbbplbjppmandaplonida',
                function(msg) {
                        location.reload();
                },
                function(error){
                        console.log(error);
			window.location.replace('/')
                });
	document.getElementById('installModal').style.display = 'none';
}


function initializeSession2(){
	var extensionId = 'faidodiononpbbplbjppmandaplonida';
    // If you register your domain with the the Firefox screen-sharing whitelist, instead of using
    // a Firefox screen-sharing extension, set this to the Firefox version number, such as 36, in which
    // your domain was added to the whitelist:
    var ffWhitelistVersion; // = '36';
    var session = OT.initSession(apiKey, sessionId);
    session.connect(token, function(error) {
      if (error) {
        alert('Error connecting to session: ' + error.message);
        return;
      }
      // publish a stream using the camera and microphone:
      var publisher = OT.initPublisher('camera-publisher');
      session.publish(publisher);
      console.log(accountType);

      if(accountType == 'teacher'){
	screenshare(session);
      }

      //document.getElementById('shareBtn').disabled = false;
    });
    session.on('streamCreated', function(event) {
      if (event.stream.videoType === 'screen') {
        // This is a screen-sharing stream published by another client
        var subOptions = {
          width: '100%',
          height: '960px'
        };
        session.subscribe(event.stream, 'screen-subscriber', subOptions);
      } else {
        // This is a stream published by another client using the camera and microphone
        session.subscribe(event.stream, 'camera-subscriber');
      }
    });
    // For Google Chrome only, register your extension by ID,
    // You can find it at chrome://extensions once the extension is installed
    OT.registerScreenSharingExtension('chrome', extensionId, 2);
}



function screenshare(session) {
	OT.checkScreenSharingCapability(function(response) {
        console.info(response);
        if (!response.supported || response.extensionRegistered === false) {
          alert('This browser does not support screen sharing.');
        } else if (response.extensionInstalled === false
            && (response.extensionRequired || !ffWhitelistVersion)) {
          alert('Please install the screen-sharing extension and load this page over HTTPS.');
        } else if (ffWhitelistVersion && navigator.userAgent.match(/Firefox/)
          && navigator.userAgent.match(/Firefox\/(\d+)/)[1] < ffWhitelistVersion) {
            alert('For screen sharing, please update your version of Firefox to '
              + ffWhitelistVersion + '.');
        } else {
          // Screen sharing is available. Publish the screen.
          // Create an element, but do not display it in the HTML DOM:
          var screenContainerElement = document.createElement('div');
          var screenSharingPublisher = OT.initPublisher(
            screenContainerElement,
            { 
		videoSource : 'screen'
	    },
            function(error) {
              if (error) {
                alert('Something went wrong: ' + error.message);
              } else {
                session.publish(
                  screenSharingPublisher,
                  function(error) {
                    if (error) {
                      alert('Something went wrong: ' + error.message);
                    }
                  });
              }
            });
          }
        });      
}
