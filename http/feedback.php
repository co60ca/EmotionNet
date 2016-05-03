<?php

include "config.php";

if (!isset($_POST)) {
  header('HTTP/1.1 403 Forbidden');
  exit(1);
}

$data = json_decode(file_get_contents("php://input"), true, 3);
$image = $data["img"];
$correct = $data["correct"];
$choice = $data["choice"];

$pathtofile = $target_dir . $image;
$basename = basename($pathtofile);
if (!file_exists($pathtofile)) {
  header('HTTP/1.1 403 Forbidden');
  exit(1);
}
$extension = "_" . ($correct == true ? "c" : "i") . "_" . $choice;
$newname = nameappend($basename, $extension);

if (!rename($pathtofile, $outputdir . $newname)) {
  header('HTTP/1.1 403 Forbidden');
  exit(1);
}

function nameappend($filename, $appendtext) {
  $fileType = pathinfo($filename, PATHINFO_EXTENSION);
  return basename($filename, ".". $fileType) . $appendtext . "." . $fileType;
}

echo "{\"msg\": \"Thanks!\"}";
