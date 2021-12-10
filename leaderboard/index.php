<?php

$cookiefile = dirname($_SERVER['DOCUMENT_ROOT'],2)."/storage/adventofcode2021-cookie.txt";

if(isset($_GET['id']))
	$board = intval($_GET['id']);
else
	$board = 380357;

$max_age = 15 * 60; # 15 minutes in seconds

$cachefile = "cache/$board.json";

# function to print terse date/timestamps
function leaderboard_time($ts, $day) {

    if($day == 'today')
        $day = date('j');
        
    $tsday = date('j',$ts);
    
    if($day == $tsday)
        return date('H:i',$ts);
	else
        return date('j-m H:i',$ts);

}

# get latest version from AoC and save cachefile
if(!file_exists($cachefile) || filemtime($cachefile) < time() - $max_age) {
	
    $url = "https://adventofcode.com/2021/leaderboard/private/view/$board.json";
	
	$cookie = trim(file($cookiefile)[0]);
	$headers = array('Cookie: '.$cookie);
	
	$ch = curl_init();
	curl_setopt($ch, CURLOPT_URL, $url);
	curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
	curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
	
	$json = curl_exec($ch);
	curl_close($ch);
	
	if(strlen($json) > 0) file_put_contents($cachefile, $json);
	
	$data_age = time();
	
} else {
	
	$json = file_get_contents($cachefile);
	$data_age = filemtime($cachefile);
}

$json = json_decode($json, true);

?>
<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<title>AoC Leaderboard <?php echo $board; ?></title>
	<style>
		html, body {margin: 0px; padding: 0px;}
		.mtime {font-family: monospace; position: fixed; top: 0px; right: 0px; margin: 16pt; padding: 0px;}
		.member {white-space: pre; font-family: monospace; margin: 16pt; padding: 0px;}
		.name {font-weight: bold;}
		.dt {color: #AAA;}
	</style>
</head>
<body><div class='mtime'>last update: <?php echo leaderboard_time($data_age, 'today');?></div><?php

usort($json['members'], function ($a, $b) {
    return -1 * ($a['local_score'] <=> $b['local_score']);
});

foreach($json['members'] as $member) {
	print("<div class='member'>");
	print("<span class='name'>$member[name]</span> ⭐️$member[stars] 🏅$member[local_score]\n");
	print("last activity: ".leaderboard_time($member['last_star_ts'],'today'));
	
	ksort($member['completion_day_level']);
	foreach($member['completion_day_level'] as $day=>$parts) {
		print("\nday ".str_pad($day,2,"0", STR_PAD_LEFT).": ");
		ksort($parts);
		foreach($parts as $part=>$time) {
			print_r(leaderboard_time($time['get_star_ts'],$day));
			if($part == 1 && count($parts) > 1) print(' / ');
		}
		if(count($parts) > 1) print(" <span class='dt'>∆t ".intval(($parts[2]['get_star_ts']-$parts[1]['get_star_ts'])/60).'min</span>');
	}
	print("</div>\n");
}

?></body>
</html>