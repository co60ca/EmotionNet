<?php

include "config.php";

$filename = basename($_GET['file']);

$file_extension = strtolower(substr(strrchr($filename,"."),1));

switch( $file_extension ) {
    case "gif": $ctype="image/gif"; break;
    case "png": $ctype="image/png"; break;
    case "jpeg":
    case "jpg": $ctype="image/jpeg"; break;
    default:
    header('HTTP/1.1 403 Forbidden');
}

header('Content-type: ' . $ctype);

// Check the folder location to avoid exploit
if (dirname($target_dir . "/" . $filename) == $target_dir)
    echo file_get_contents($target_dir . "/" . $filename);
