<?php

$cookiefile = dirname($_SERVER['DOCUMENT_ROOT'],2)."/storage/adventofcode2021-cookie.txt";

if(isset($_GET['id']))
	$board = intval($_GET['id']);
else
	$board = 380357;

if(isset($_GET['year']))
	$year = intval($_GET['year']);
else
	$year = 2021;

$userpages = array( 379312 => "https://github.com/EagleErwin/AdventOfCode/tree/master/$year",
			  	    380357 => "https://github.com/HarmtH/aoc/tree/master/$year",
				    380677 => "https://github.com/apie/advent-of-code/tree/master/$year",
				   1616236 => "https://github.com/cwverhey/adventofcode",
				   1838848 => "https://github.com/leonschenk/codeofadvent");

$max_age = 10 * 60; # 10 minutes in seconds

$cachefile = "cache/$board-$year.json";

$years = range(intval(date('Y'))-1, 2015, -1);
if(date('m') == '12') array_unshift($years, intval(date('Y')));

$days = range(1,25);
if($year == date('Y') && date('j') <= 25) {
	if(date('G') >= 6) $days = range(1, date('j'));
	else $days = range(1, date('j')-1);
}


# function to print terse date/timestamps
function leaderboard_time($ts, $day) {
	
	global $year;

	if($ts == 0)
		return('-');

    if($day == 'today') 
        $day = date('j');
        
    if(date('j-n-Y',$ts) == $day+'12'+$year)
        return date('H:i',$ts);
	
    if(date('Y',$ts) == $year)
		return date('j-n H:i',$ts);
    
	return date('j-n-Y H:i',$ts);

}

# get latest version from AoC and save cachefile
if(!file_exists($cachefile) || filemtime($cachefile) < time() - $max_age) {
	
    $url = "https://adventofcode.com/$year/leaderboard/private/view/$board.json";
	
	$cookie = trim(file($cookiefile)[0]);
	$headers = array('Cookie: '.$cookie);
	
	$ch = curl_init();
	curl_setopt($ch, CURLOPT_URL, $url);
	curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
	curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
	
	$json = curl_exec($ch);
	
	curl_close($ch);
	
	if(count(json_decode($json, true)) > 0) file_put_contents($cachefile, $json);
	
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
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<title>Advent of Code Leaderboard #<?php echo $board; ?></title>
	<style>
		html, body {margin: 0px; padding: 0px;}
		.mtime {font-family: monospace; position: fixed; top: 0px; right: 0px; margin: 16pt; padding: 0px; line-height: 150%;}
		.member {white-space: pre; font-family: monospace; margin: 16pt; padding: 0px;}
		.name {font-weight: bold;}
		.lastact {line-height: 200%;}
		.dt {color: #AAA;}
		.yearform {display: inline; font-family: monospace;}
		#year {font-family: monospace;}
		a {color: #000; text-decoration-style: dotted; text-decoration-color: #BBB;}
	</style>
</head>
<body>

<div class='mtime'>
	
	year: <form action='' class='yearform'>
	<select name="year" id="year" onchange="this.form.submit()">
	<?php
	foreach($years as $y) {
		if($y == $year)
			print("\t<option value=$y selected>$y</option>\n");
		else
			print("\t<option value=$y>$y</option>\n");
	}
	?>
	</select>
	<noscript><input type="submit" value="go"></noscript>
	</form><br />
	
	last update: <?php echo leaderboard_time($data_age, 'today');?><br />
	<a href='https://adventofcode.com/<?php echo $year; ?>/leaderboard/private/view/<?php echo $board; ?>'>AoC page</a>
	
	
</div>

<?php

if($json) {

	usort($json['members'], function ($a, $b) {
		if($a['stars'] < $b['stars']) return 1;
		if($a['stars'] > $b['stars']) return -1;
	
		if($a['local_score'] < $b['local_score']) return 1;
		if($a['local_score'] > $b['local_score']) return -1;
	
		return -1 * ($a['name'] <=> $b['name']);
	});

	foreach($json['members'] as $member) {
		print("<div class='member'>");
		if(array_key_exists($member['id'],$userpages))
			print("<span class='name'><a href='".$userpages[$member['id']]."' target='_blank'>$member[name]</a></span> ⭐️$member[stars] 🏅$member[local_score]\n");
		else
			print("<span class='name'>$member[name]</span> ⭐️$member[stars] 🏅$member[local_score]\n");
			
		print("<span class='lastact'>last activity: ".leaderboard_time($member['last_star_ts'],'today')."</span>");
	
		ksort($member['completion_day_level']);
		
		foreach($days as $day) {
			print("\nday ".str_pad($day,2,"0", STR_PAD_LEFT).": ");
			
			if(array_key_exists($day, $member['completion_day_level'])) {
				$parts = $member['completion_day_level'][$day];
				ksort($parts);
				foreach($parts as $part=>$time) {
					print_r(leaderboard_time($time['get_star_ts'],$day));
					if($part == 1) print(' / ');
					if(count($parts) == 1) print('-');
				}
				if(count($parts) > 1) print(" <span class='dt'>∆t ".round(($parts[2]['get_star_ts']-$parts[1]['get_star_ts'])/60).'min</span>');
				
			} else {
				print('-');
			}
		}
		print("</div>\n");
	}

} else {
	print("Failed to retrieve leaderboard for board id=$board, year=$year");
}
?>
</body>
</html>