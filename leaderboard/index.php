<?php

#
# load options/variables
#

if ($_SERVER['HTTP_HOST'] == '192.168.1.2') {
    $cookiefile = "/home/caspar/.config/adventofcode-cookie.txt"; // must look like: "session=f0oBaRbaz"
    $max_age = 1000 * 60; // max cache age
} else {
    $cookiefile = dirname($_SERVER['DOCUMENT_ROOT'],2)."/storage/adventofcode-cookie.txt"; // must look like: "session=f0oBaRbaz"
    $max_age = 10 * 60; // max cache age
}

if(isset($_GET['id'])) {
    $board = intval($_GET['id']);
} else {
    $board = 380357;
}

if(isset($_GET['year'])) {
    $year = intval($_GET['year']);
} else {
    if(date('n') < 12) { // if month < 12:
        $year = date('Y') - 1; // previous year
    } else {
        $year = date('Y'); // current year
    }
}

$userpages = array( 379312 => "https://github.com/EagleErwin/AdventOfCode/tree/master/$year",
                    380357 => "https://github.com/HarmtH/aoc/tree/master/$year",
                    380677 => "https://github.com/apie/advent-of-code/tree/master/$year",
                   1616236 => "https://github.com/cwverhey/adventofcode/tree/main/$year",
                   1838848 => "https://github.com/leonschenk/codeofadvent/tree/main/$year");

$cachefile = "cache/$board-$year.json";

$years = range(date('Y')-1, 2015, -1); // first AoC edition was 2015
if(date('m') == '12') array_unshift($years, intval(date('Y'))); // add current year if month ≥ 12

$days = range(1,25);
if($year == date('Y') && date('j') <= 25) { // limit day range if from 1-24 december:
    if(date('G') >= 6) { // if after 6 AM local time:
        $days = range(1, date('j')); // include today
    } else {
        $days = range(1, date('j')-1); // exclude today
    }
}

#
# function definitions
#

# print terse date/timestamps for 'last active' and task completion times
function leaderboard_time($ts, $reference_day) {

    global $year;

    if($ts == 0) return('-');

    if($reference_day == 'today') $reference_day = date('j'); // j = day of the month without leading zeros

    $span = '<span title="'.date('d-m-Y H:i:s',$ts).'" tabindex=0>';

    if(date('j-n-Y',$ts) == $reference_day.'-12-'.$year) { // if $ts is on the reference day:
        $span .= date('H:i',$ts);
    } elseif(date('Y',$ts) == $year) { // elseif $ts is in the reference year:
        $span .= date('d-m',$ts);
    } else { // else:
        $span .= date('d-m-Y',$ts);
    }

    $span .= '</span>';

    return $span;

}


# print terse date/timestamps for last cache update
function last_update_time($ts) {

    if($ts == 0) return('-');
    
    $span = '<span title="'.date('d-m-Y H:i:s',$ts).'" tabindex=0>';

    if(date('j-n-Y',$ts) == date('j-n-Y')) { // if $ts is today:
        $span .= date('H:i',$ts);
    } else {
        $span .= date('d-m-Y H:i',$ts);
    }

    $span .= '</span>';

    return $span;

}


# function to print delta t
function dt($time1, $time2) {

    $dt = $time2 - $time1;

    if ($dt < 99.5) {
        $short = $dt.'s';
        $long = $dt.'s';
    } else if ($dt < 99.5 * 60) {
        $short = round($dt/60).'m';
        $long = floor($dt/60).'m '.($dt%60).'s';
    } else if ($dt < 99.5 * 60 * 48) {
        $short = round($dt/(60*60)).'h';
        $long = floor($dt/(60*60)).'h '.floor(($dt%(60*60))/60).'m '.($dt%60).'s';
    } else {
        $short = round($dt/(60*60*24)).'D';
        $long = floor($dt/(60*60*24)).'D '.floor(($dt%(60*60*24))/(60*60)).'h '.floor(($dt%(60*60))/60).'m '.($dt%60).'s';
    }

    $span = '<span class="dt" title="∆ '.$long.'" tabindex=0>∆ ';
    $span .= str_pad($short, 3, ' ', STR_PAD_LEFT);
    $span .= '</span>';

    return $span;

}

#
# get leaderboard data
#

# get new data from AoC server
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

    if(!empty(json_decode($json, true))) file_put_contents($cachefile, $json); // save cache file

}

# load from cache file
$json = @file_get_contents($cachefile); // suppress warning
if ($json === false) {
    http_response_code(404);
    exit("ERROR: could not load leaderboard data. Change your request parameters or retry at a later time.");
}
$json = json_decode($json, true);

# get cache file modification time
clearstatcache();
$data_time = filemtime($cachefile);

# group users/members into df by stars
$df = array();
foreach($json['members'] as $m) {

    # remove a level of depth in time-array
    foreach ($m['completion_day_level'] as $d => $v) {
        foreach ($v as $p => $s) {
            $m['completion_day_level'][$d][$p] = $m['completion_day_level'][$d][$p]['get_star_ts'];
        }
        ksort($m['completion_day_level'][$d]);
    }

    # sort time-array
    ksort($m['completion_day_level']);

    # add member to df
    $df[$m['stars']][] = $m;
}

# shuffle users per star level
foreach($df as $stars => $v) {
    shuffle($v);
    $df[$stars] = $v;
}

# sort dataframe by stars, descending
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
        
        .mtime {position: fixed; top: 0px; right: 0px; margin: 8pt; padding: 8pt; line-height: 150%; background-color: rgba(255, 255, 255, 0.8);}
        .yearform {display: inline;}
        #year {font-family: monospace;}
        .darkmodetoggle.light {display: none;}

        .row {white-space: pre; padding-left: 50pt; padding-right: 100pt; clear: left;}
        .stars {padding: 10pt; width: 40pt; font-size: 300%; text-align: center; position: absolute; left: 0;}
        .user {float: left; padding: 10pt; }

        .name {font-weight: bold;}
        .lastact {line-height: 200%;}
        .dt {color: #AAA;}

        body.dark {
            color-scheme: dark;
            color: #6f6f6f;
            background-color: #15191d;
            & a {color: #6f6f6f; text-decoration-color: #6f6f6f;}
            .mtime {background-color: #15191d}
            .dt {color: #4e4e4e;}
            .darkmodetoggle.light {display: unset;}
            .darkmodetoggle.dark {display: none;}
        }

        @media (pointer: coarse), (hover: none) {
            [title] {
                position: relative;
                display: inline-flex;
                justify-content: left;
                z-index: auto;
                line-height: 100%; 
            }
            [title]:focus::after {
                content: attr(title);
                position: absolute;
                top: 0;
                padding: 0;
                margin: 0;
                background-color: #DDD;
                z-index: 1;
            }
        }

    </style>
    <script>
        function toggleDarkMode() {
            document.body.classList.toggle('dark');
            localStorage.setItem('darkmode', document.body.classList.contains('dark'));
        }

        window.addEventListener('load', function () {
            if (localStorage.getItem('darkmode') === undefined) {
                if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
                    localStorage.setItem('darkmode', true);
                }
            }
            if (localStorage.getItem('darkmode') === 'true') {
                toggleDarkMode();
            }
        });
    </script>
</head>
<body>

<div class='mtime'>

    year: <form action='' class='yearform'>
    <select name="year" id="year" onchange="this.form.submit()">
    <?php
    foreach($years as $y) {
        if($y == $year) {
            print("\t<option value=$y selected>$y</option>\n");
        } else {
            print("\t<option value=$y>$y</option>\n");
        }
    }
    ?>
    </select>
    <noscript><input type="submit" value="go"></noscript>
    </form><br />

    last update: <?php echo last_update_time($data_time); ?><br />
    <a href='https://adventofcode.com/<?php echo $year; ?>/leaderboard/private/view/<?php echo $board; ?>'>AoC page</a>
    <a href="#" onclick="toggleDarkMode('dark'); return false;" class="darkmodetoggle dark">🌖</a>
    <a href="#" onclick="toggleDarkMode('light'); return false;" class="darkmodetoggle light">🌘️</a>

</div>

<?php

foreach($df as $stars => $users) {

    print("<div class='row'>\n");
    
    print("<div class='stars'>⭐️<br />$stars</div>");

    foreach($users as $user) {
        
        print('<div class="user">');
        
        print('<span class="name">');
        if(array_key_exists($user['id'],$userpages)) {
            print("<a href='".$userpages[$user['id']]."' target='_blank'>$user[name]</a>");
        } else {
            print($user['name']);
        }
        print("</span> 🏅$user[local_score]\n");
            
        print("<span class='lastact'>last activity: ".leaderboard_time($user['last_star_ts'],'today')."</span>");

        foreach($days as $day) {
            print("\nday <a href=\"https://adventofcode.com/".$year."/day/".$day."\">".str_pad($day,2,"0", STR_PAD_LEFT)."</a>: ");
            
            if(array_key_exists($day, $user['completion_day_level'])) {
                print(leaderboard_time($user['completion_day_level'][$day][1],$day));
                print(' / ');
                if(count($user['completion_day_level'][$day]) == 2) {
                    print(leaderboard_time($user['completion_day_level'][$day][2],$day));
                    print('&nbsp;&nbsp;');
                    print(dt($user['completion_day_level'][$day][1],$user['completion_day_level'][$day][2]));
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

?>
</body>
</html>