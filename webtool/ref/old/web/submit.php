<?php 
    header("Content-type:text/html;charset=utf-8");
    header('Access-Control-Allow-Origin:*');

    // 获取Ajax提交的数据
    $pointdata = @$_POST['pointdata'];
    $reduce_rate = @$_POST['reduce_rate'];
    $tolerance_of_edge_length = @$_POST['tolerance_of_edge_length'];
    $length_constraint_maltiplier = @$_POST['length_constraint_maltiplier'];
	$boundary_constraint_magnitude = @$_POST['boundary_constraint_magnitude'];
    $perp_steps = @$_POST['perp_steps'];
    $minumum_radius = @$_POST['minumum_radius'];
    $maximum_radius = @$_POST['maximum_radius'];
	
	//mySQL连接
    $link = mysqli_connect(
        'localhost:3307',
        'root',
        '15935755a',
        'DFW'
    );
    if (!$link) {
        printf("Can't connect to MySQL Server. Errorcode: %s ", mysqli_connect_error());
        exit;
    }
    mysqli_set_charset($link,'utf8');

	$sql ="insert into gh (pointdata, reduce_rate, tolerance_of_edge_length, length_constraint_maltiplier, boundary_constraint_magnitude, perp_steps, minumum_radius, maximum_radius) VALUES ('"
	.$pointdata.     "','"
	.$reduce_rate.    "','"
	.$tolerance_of_edge_length.  "','"
	.$length_constraint_maltiplier.   "',"
	.$boundary_constraint_magnitude.   "',"
	.$perp_steps.   "',"
	.$minumum_radius.   "',"
	.$maximum_radius.   "',";
	mysqli_query($link, $sql);

	echo 200;  // 提交成功
	
	// 关闭数据库连接
    mysqli_close($link);
	
 ?>