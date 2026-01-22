<?php 
	$id = isset($_GET['c']) ? $_GET['c'] : '';
	$val = isset($_GET['v']) ? $_GET['v'] : '';

	function generateUuidv4()
	{
	return sprintf('%04x%04x-%04x-%04x-%04x-%04x%04x%04x',mt_rand(0, 0xffff),mt_rand(0, 0xffff),mt_rand(0, 0xffff),
	mt_rand(0, 0x0fff) | 0x4000,mt_rand(0, 0x3fff) | 0x8000,mt_rand(0, 0xffff),mt_rand(0, 0xffff),mt_rand(0, 0xffff));
	}

	function makeLink()
	{
	global $id,$key;
	$track = ( $key == 0 ) ? 1 : 0;
	$data = "https://cfd-v4-service-channel-stitcher-use1-1.prd.pluto.tv/stitch/hls/channel/".$id."/master.m3u8?".
	"appName=web&appVersion=unknown&appStoreUrl=&architecture=&buildVersion=&clientTime=0&deviceId=".generateUuidv4().
	"&deviceVersion=unknown&includeExtendedEvents=false&sid=".generateUuidv4()."&userId=&serverSideAds=true".
	"&deviceType=".($track?"samsung-tvplus":"web").
	"&deviceMake=".($track?"samsung":"Chrome").
	"&deviceModel=".($track?"samsung":"web").
	"&deviceDNT=".($track?"%7BTARGETOPT%7D":"0").
	"&advertisingId=".($track?"%7BPSID%7D":"");
	if( $track ) $data .= "&us_privacy=%7BUS_PRIVACY%7D&samsung_app_domain=%7BAPP_DOMAIN%7D&samsung_app_name=%7BAPP_NAME%7D&embedPartner=samsung-tvplus&gdprConsent=%7BTC_STRING%7D&gdpr=1&deviceLat=0&deviceLon=0";
	return $data;
	}
	
	$key = preg_replace('/[^0-9]/','',$val);
	$url = makeLink();

	if ( $key == 100 )
	{
	echo '#EXTM3U\n#EXTINF:0, Pluto TV\n'.$url.'\n';
	}
	else
	{
	header("Location: ".$url);
	}
?>
