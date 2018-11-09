<html>
<head>
	<title>PHP SCRIPT</title>
	<style>
		body {background-color:CornflowerBlue;}
		table, th, td {border: 1px solid black; border-collapse:collapse; background-color:white; color:black; text-align:center;}
		table td {background-color:black; color:white;}
		a:link { color:white;}
		a:visited {color:CornflowerBlue;}
		a:hover {color:white;}
	</style>
</head>
<body>
<table align="center">
	<?php
		$conn = mysqli_connect("localhost", "cs288", "CS288.pass", "stockmarket");
		
		if(isset($_GET['order'])){ #column by which it orders it
			$order = $_GET['order'];
		}
		else{
			$order = 'volume'; #default value=name	
		}
		if(isset($_GET['sort'])){ #column by which it sorts it
			$sort = $_GET['sort'];
		}
		else{
			$sort = 'ASC'; #default value= descedning order	
		}

		
		$sort == "DESC" ? $sort = "ASC" : $sort = "DESC";
		#$db = mysql_select_db("stockmarket");
		$table = "2017_12_02_11_32_56";#"timestamp";
		$query = "select * from $table order by $order $sort"; #order asset# by asc
		$rows = mysqli_query($conn, $query);
		$ncols = mysqli_num_fields($rows);
		echo("<tr>");
		/*for ($col=0; $col<$ncols; $col++){
			$field = mysqli_fetch_field_direct($rows, $col)->name;
			#echo($field);
			echo("<th><a href='?order=volume'> $field </a></th>");
		}#will have the name of the cols; name of cols in table database*/
		echo("<td><a href='?order=name&&sort=$sort'> name </a></td>");
		echo("<td><a href='?order=symbol&&sort=$sort'> symbol </a></td>");
		echo("<td><a href='?order=volume&&sort=$sort'> volume </a></td>");
		echo("<td><a href='?order=price&&sort=$sort'> price </a></td>");
		echo("<td><a href='?order=chng&&sort=$sort'> change </a></td>");
		echo("<td><a href='?order=pchng&&sort=$sort'> %change </a></td>");
		echo("</tr>");

		while($row = mysqli_fetch_row($rows)){
			echo("<tr>");
			for ($col=0; $col<$ncols; $col++){
				echo("<th> $row[$col] </th>");
			}
			echo("</tr>");
		}
	?>
</table>
</body>
</html>
