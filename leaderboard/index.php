
<?php

# load options/variables
if ($_SERVER['HTTP_HOST'] == '192.168.1.2') {
	$cookiefile = "/home/caspar/.config/adventofcode-cookie.txt";
	$max_age = 1000 * 60;
} else {
	$cookiefile = dirname($_SERVER['DOCUMENT_ROOT'],2)."/storage/adventofcode-cookie.txt";
	$max_age = 10 * 60;
}

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
	
	$title = '<span title="'.date('d-m-Y H:i:s',$ts).'">';
        
    if(date('j-n-Y',$ts) == $day.'-12-'.$year)
        return $title.date('H:i',$ts).'</span>';
	
    if(date('Y',$ts) == $year)
		return $title.date('d-m',$ts).'</span>';
    
	return $title.date('d-m-Y',$ts).'</span>';

}


# function to print terse date/timestamps for last update
function last_update_time($ts) {
	
	if($ts == 0)
		return('-');
    
	$title = '<span title="'.date('d-m-Y H:i:s',$ts).'">';
        
    if(date('j-n-Y',$ts) == date('j-n-Y'))
        return $title.date('H:i',$ts).'</span>';
	
	return $title.date('d-m-Y H:i',$ts).'</span>';

}


# function to print delta t
function dt($time1, $time2) {
	
	$dt = $time2 - $time1;
	
	if ($dt < 99.5) $str = $dt.'s';
	
	else if ($dt < 99.5 * 60) $str = round($dt/60).'m';
	
	else if ($dt < 99.5 * 60 * 48) $str = round($dt/(60*60)).'H';
	
	else $str = round($dt/(60*60*24)).'D';
	
	return str_pad($str, 3, ' ', STR_PAD_LEFT);
		
}


# get latest version from AoC and save cachefile
$data_time = 0;
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
	
	if(!empty(json_decode($json, true))) {
		file_put_contents($cachefile, $json);
		$data_time = time();
	}
	
}

if($data_time == 0) {
	
	$json = file_get_contents($cachefile);
	$data_time = filemtime($cachefile);
}

$json = json_decode($json, true);


# group users into df by stars
$df = array();
foreach($json['members'] as $m) {
	
	# remove a level of depth in time-array
	foreach ($m['completion_day_level'] as $d => $v) {
		foreach ($v as $p => $s)
			$m['completion_day_level'][$d][$p] = $m['completion_day_level'][$d][$p]['get_star_ts'];
		ksort($m['completion_day_level'][$d]);
	}
	
	# sort time-array
	ksort($m['completion_day_level']);
		
	# set member in df	
	$df[$m['stars']][] = $m;
}

# sort df
foreach($df as $stars => $v) {
	shuffle($v);
	$df[$stars] = $v;
}
krsort($df);

?>
<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<title>Advent of Code Leaderboard #<?php echo $board; ?></title>
	<style>
		
		html, body {margin: 0px; padding: 0px; font-family: monospace;}
		a {color: #000; text-decoration-style: dotted; text-decoration-color: #BBB;}
		
		.mtime {position: fixed; top: 0px; right: 0px; margin: 16pt; padding: 0px; line-height: 150%;}
		.yearform {display: inline;}
		#year {font-family: monospace;}
		
		.row {white-space: pre; padding-left: 50pt; clear: left;}
		.stars {padding: 10pt; width: 40pt; font-size: 300%; text-align: center; position: absolute; left: 0;}
		.user {float: left; padding: 10pt; }
		
		.name {font-weight: bold;}
		.lastact {line-height: 200%;}
		.dt {color: #AAA;}
		
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
	
	last update: <?php echo last_update_time($data_time);?><br />
	<a href='https://adventofcode.com/<?php echo $year; ?>/leaderboard/private/view/<?php echo $board; ?>'>AoC page</a>
	
	
</div>

<?php

foreach($df as $stars => $users) {
	
	print("<div class='row'>\n");
	print("<div class='stars'>??????<br />$stars</div>");
	
	foreach($users as $user) {
		
		print('<div class="user">');
		
		print('<span class="name">');
		if(array_key_exists($user['id'],$userpages))
			print("<a href='".$userpages[$user['id']]."' target='_blank'>$user[name]</a>");
		else
			print($user['name']);
		print("</span> ????$user[local_score]\n");
			
		print("<span class='lastact'>last activity: ".leaderboard_time($user['last_star_ts'],'today')."</span>");
	
		foreach($days as $day) {
			print("\nday ".str_pad($day,2,"0", STR_PAD_LEFT).": ");
			
			if(array_key_exists($day, $user['completion_day_level'])) {
				print(leaderboard_time($user['completion_day_level'][$day][1],$day));
				print(' / ');
				if(count($user['completion_day_level'][$day]) == 2) {
					print(leaderboard_time($user['completion_day_level'][$day][2],$day));
					print(' <span class="dt"> ??? '.dt($user['completion_day_level'][$day][1],$user['completion_day_level'][$day][2]).'</span>');
				} else {
					print('-');
				}
			} else {
				print('-');
			}
		}
		print("</div>");
		
		
		
	}
	
	print("</div>\n\n");
}

#print("Failed to retrieve leaderboard for board id=$board, year=$year");

?>
</body>
</html>