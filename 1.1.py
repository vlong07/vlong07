<?php
use Slim\Factory\AppFactory;
use Psr\Http\Message\ResponseInterface as Response;
use Psr\Http\Message\ServerRequestInterface as Request;

require __DIR__ . '/vendor/autoload.php';

// Initialize Slim App
$app = AppFactory::create();

// Define your routes
$app->get('/shorten', function (Request $request, Response $response, $args) {
    $queryParams = $request->getQueryParams();

    // Your existing logic here
    $txt = substr(md5(date('dmY')."toolvip".$_SERVER['REMOTE_ADDR']), 0 , 8);
    $linkkey = urlencode("https://luvanlong.000webhostapp.com/key.html?key=$txt");
    $response = requests("https://link4m.co/api-shorten/v2?api=65379f5858dd661f121ed632&url=".$linkkey);

    if ($response->status == "success" and $linkkey != '') {
        $responseData = [
            "success" => '200',
            "key" => $txt,
            "link" => $response->shortenedUrl,
            "ip" => $_SERVER['REMOTE_ADDR'],
        ];
    } else {
        $responseData = [
            "link" => 'Hãy Dùng Key Phí',
            "ip" => $_SERVER['REMOTE_ADDR'],
        ];
    }

    // Return JSON response
    $response->getBody()->write(json_encode($responseData));
    return $response
        ->withHeader('Content-Type', 'application/json')
        ->withStatus(200);
});

// Helper function for making requests
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
    curl_close($ch);
    return json_decode($response);
}

// Run Slim App
$app->run();
?>
