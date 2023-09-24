<!DOCTYPE html>
<html>
	<head>
		<meta http-equiv="refresh" content="5">
		<meta charset="utf-8" />
		<title>Groupe 1 - GUI</title>
		<?php
		$atl = new PDO(
			'mysql:host=localhost;dbname=atl;charset=utf8',
			'groupe1',
			'2067',
			[PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION]
		);
		$atlDiagnos = $atl->prepare('SELECT * FROM status');
		$atlDiagnos->execute();
		$atlStatus = $atlDiagnos->fetchAll();
		?>
		<?php foreach ($atlStatus as $atlState) {
			if($atlState['auto_command']==false && $atlState['on_pompe']==true)
				$atlDiagnos = $atl->prepare('UPDATE status SET on_pompe = false');
				$atlDiagnos->execute();
			if($atlState['auto_command']==false && $atlState['on_pompe']==false)
				$atlDiagnos = $atl->prepare('UPDATE status SET on_pompe = true');
				$atlDiagnos->execute();
		?>
		<?php
			}?>
		<?php header('location: gui.php');
		?>