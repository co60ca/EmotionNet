<?php


# The MIT License (MIT)
#
# Copyright (c) 2016 Maeve Kennedy
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


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
