$('#submit').click(function(e){
    e.preventDefault()
    var formData = new FormData($('#form')[0]);
    $.ajax({
        url: 'upload.php',  //Server script to process data
        type: 'POST',
        xhr: function() {  // Custom XMLHttpRequest
            var myXhr = $.ajaxSettings.xhr();
            if(myXhr.upload){ // Check if upload property exists
                myXhr.upload.addEventListener('progress',progressHandlingFunction, false); // For handling the progress of the upload
            }
            return myXhr;
        },
        //Ajax events
        beforeSend: beforeSendHandler,
        success: completeHandler,
        error: errorHandler,
        // Form data
        data: formData,
        dataType: 'json',
        //Options to tell jQuery not to process data or worry about content-type.
        cache: false,
        contentType: false,
        processData: false
    });
});

$('#restart').click(function(){
  $("#uploadFile").replaceWith($("#uploadFile").val('').clone(true));
  $("#resultsbox").hide();
  $("#feedbackboxtop").show();
  $("#feedbackbox").hide();
  $("#thanksbox").hide();
  $("#form").show();
});

function beforeSendHandler(e){
  $("#form").hide();
  $("#progressbox").show();
  intervalupdate = setInterval(function(){
    var text = "";
    switch (stringnumdiffwords) {
      case 0: text = "This can't take longer than 30 seconds!"; break;
      case 1: text = "GPUs would make this faster, but they are quite expensive!"; break;
      case 2: text = "I swear this worked better in testing."; break;
      case 3: text = "Please provide feedback through the form, it helps the model be more general!"; break;
      case 4: text = "The images seem to work better if composed like a passport photo."; break;
      case 5: text = "If it doesn't work please give us advice to what you think it should have been!"; break;
      case 6: text = "We check all the images, so don't try and break it!"; break;
      case 7: text = "Smaller images work better!"; break;
      case 8: text = "Cats might work too!"; break;
      case 9: text = "You've been waiting for awhile..."; break;
      case 10: text = "Don't worry, it should tell you if something went wrong!"; break;
      case 11: text = "We spent awhile ensuring this page was robust."; break;
      case 12: text = "So... have you watched any good movies lately?"; break;
      case 13: text = "Zootopia was pretty good, I'd check it out."; break;
      case 14: text = "They made lots of references to old-timey movies."; break;
      case 15: text = "No one in the theater got the references..."; break;
    }
    $("#differentwords").text(text);
    if (++stringnumdiffwords > 15) stringnumdiffwords = 0;
  }, 4500);
}

function displayError(text) {
  $("#progressbox").text(text);
  $("#progressbox").show();
}

// We set the imagename here so we can use it elsewhere without a lookup
var imagename = null;
var classnumber = null;
var intervalupdate = null;
var stringnumdiffwords = 0;

function completeHandler(e) {
  $("#progressbox").hide();
  if (e.error != null) {
    displayError("Error: Either image was invalid format, or too large 2MB is the " +
                 "maximum file size.");
    console.log(e);
    return;
  }
  imagename = e.imagename;
  classnumber = e.class;

  var classname = "";
  switch(classnumber) {
    case 0: classname = "a neutral expression"   ; break;
    case 5: classname = "a happy expression" ; break;
    case 1: classname = "anger"     ; break;
    case 2: classname = "contempt"  ; break;
    case 3: classname = "disgust"   ; break;
    case 4: classname = "fear"      ; break;
    case 6: classname = "sadness"   ; break;
    case 7: classname = "surprise"  ; break;
    default:
      classname = "Uhh... something bad happened..."
  }

  $("#classification").text("This looks like " + classname + " to us");
  var url = "retrieveimg.php?file=" + e.imagename;
  $("#imgbox").html('<img width="250px" src="' + url + '"></img>');
  console.log(e);
  fillResultFromData(e.output_prob);
  $("#resultsbox").show();
  clearInterval(intervalupdate);
}

function errorHandler(e) {
  displayError("Error occured while uploading image");
  console.log(e);
}

function fillResultFromData(data) {
  for (i = 0; i < 8; i++) {
    $("#progress" + i).attr("aria-valuenow", data[i]);
    $("#progress" + i).text((data[i]*100).toFixed(2) + "%");
    $("#progress" + i).css("width", (data[i]*100).toFixed(2) + "%");
  }
}

function progressHandlingFunction() { }

function giveFeedBack(imagenamesend, correct, option) {
  $.post("feedback.php", JSON.stringify({"img": imagenamesend, "correct": correct, "choice": option}));
}

// Feedback loop
$("#buttonyes").click(function () {
  giveFeedBack(imagename, true, classnumber);
  $("#feedbackboxtop").hide();
  $("#thanksbox").show();
});

$("#buttonno").click(function () {
  $("#feedbackbox").show();
});

function feedbackclickfunct(i) {
  return function () {
    giveFeedBack(imagename, false, i);
    $("#feedbackboxtop").hide();
    $("#feedbackbox").hide();
    $("#thanksbox").show();
  }
}
for (var i = 0; i < 8; i++) {
  $("#feedback" + i).click(feedbackclickfunct(i));
}
