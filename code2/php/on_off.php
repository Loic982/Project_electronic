<!DOCTYPE html>
<html>
	<head>
		<meta http-equiv="refresh" content="5">  <!-- refresh la page toutes les 5s -->
		<meta charset="utf-8" />
		<title>Groupe 1 - GUI</title>
		<?php
		$atl = new PDO(
			'mysql:host=localhost;dbname=atl;charset=utf8', // connexion à MySQL
			'groupe1',
			'2067',
			[PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION] // permet de gérer les erreurs de la classe PDO
		);
		$atlDiagnos = $atl->prepare('SELECT * FROM status');
		$atlDiagnos->execute();
		$atlStatus = $atlDiagnos->fetchAll();
		?>
		<?php foreach ($atlStatus as $atlState) { // système de requète
			if($atlState['auto_command']==false && $atlState['on_pompe']==true) // si on est en mode MANUEL et la pompe en ON
				$atlDiagnos = $atl->prepare('UPDATE status SET on_pompe = false'); // lorsqu'il y aura une update, la pompe est en OFF 
				$atlDiagnos->execute();
			if($atlState['auto_command']==false && $atlState['on_pompe']==false) // si on est en mode MANUEL et la pompe en OFF
				$atlDiagnos = $atl->prepare('UPDATE status SET on_pompe = true'); // lorsqu'il y aura une update, la pompe est en ON 
				$atlDiagnos->execute();
		?>
		<?php
			}?>
		<?php header('location: gui.php');
		?>















		