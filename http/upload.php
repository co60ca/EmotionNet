<?php

include "config.php";

$target_file = $target_dir . basename($_FILES["uploadFile"]["name"]);

$uploadOk = 1;
$fileType = pathinfo($target_file,PATHINFO_EXTENSION);
#echo $fileType;

$randomvalue = rand();

$target_file = $target_dir . $randomvalue . "." . $fileType;
// Check if image file is a actual image or fake image
if(isset($_FILES["uploadFile"])) {
    $check = getimagesize($_FILES["uploadFile"]["tmp_name"]);
    if($check !== false) {
        $uploadOk = 1;
    } else {
        $uploadOk = 0;
    }
}
$fileType = strtolower($fileType);
if ($fileType != "jpg" && $fileType != "jpeg" && $fileType != "png" && $fileType != "gif"){
  echo "File is of wrong type" . $fileType;
	$uploadOk = 0;
}

if ($uploadOk == 1){
	move_uploaded_file($_FILES["uploadFile"]["tmp_name"], $target_file);
  $curlres = curl_init();

  // set url
  curl_setopt($curlres, CURLOPT_URL, "localhost:5000?fileid=" . $target_file);

  // return the transfer as a string
  curl_setopt($curlres, CURLOPT_RETURNTRANSFER, 1);

  // $output contains the output string
  $output = curl_exec($curlres);


  // close curl resource to free up system resources
  curl_close($curlres);

  if($output === false) {
    echo "{\"error\" : \"failed to contact EmotionNet server ㅠㅠ\"}";
    exit(1);
  }

  $output = json_decode($output, true);
  $output["imagename"] = basename($target_file);
  $output = json_encode($output, JSON_UNESCAPED_SLASHES);
  echo $output;
}else{
	echo "{\"error\" : \"failed to upload file ㅠㅠ\"}";
}
