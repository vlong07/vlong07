<?php
error_reporting(0);
session_start();
date_default_timezone_set("Asia/Ho_Chi_Minh");





$useragent = "Mozilla/5.0 (Linux; Android 10; Active 3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Mobile Safari/537.36";

#$txt = substr(md5(date('dmY')."toolvip".$_SERVER['REMOTE_ADDR']), 0 , 8);

#$url = file_get_contents('https://sever.ngocbansub.com/toolmoi/api_cua_ngoc/link4m.php?txt='.$txt);
#$url= urlencode("https://ngocbansub.com/api_by_Ngoc/link.php?link=$url1");
$linkkey= urlencode("https://luvanlong.000webhostapp.com/key.html?key=$txt");
#$linkkey2 = requests('https://link4m.co/api-shorten/v2?api=6509351d4e43a927b1419322&url='.$linkkey)->shortenedUrl;
$response = requests("https://web1s.com/api?token=487d6775-92ed-414f-a6f7-089e8a5c935f&url=".$linkkey);

if($response->status == "success" and $linkkey != '') {

die(json_encode([
"success" => '200',
"key" => $txt,
"link" =>  $response->shortenedUrl,
"ip" => $_SERVER['REMOTE_ADDR'],
]));

} else {

#$url1= file_get_contents('https://sever.ngocbansub.com/api_by_Ngoc/traffic.php?txt='.$txt);
die(json_encode([
"link" =>  'Hãy Dùng Key Phí',
"ip" => $_SERVER['REMOTE_ADDR'],
"coun" => $so,
]));
}
function requests($url) {
	$ch = curl_init();
	curl_setopt_array($ch, array(
		CURLOPT_URL => $url,
		CURLOPT_CUSTOMREQUEST => "GET",
		CURLOPT_SSL_VERIFYHOST => false,
		CURLOPT_SSL_VERIFYPEER => false,
		CURLOPT_RETURNTRANSFER => true,
		CURLOPT_TIMEOUT => 15,
		CURLOPT_ENCODING => "",
		CURLOPT_FOLLOWLOCATION => true
	));
	$response = curl_exec($ch);
	return json_decode($response);
}
?>