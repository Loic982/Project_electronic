<!DOCTYPE html>
<html>
	<head>
		<meta http-equiv="refresh" content="5"> <!-- refresh la page toutes les 5s -->
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
			if($atlState['auto_command']==false && $atlState['fenetre_ouvert']==true) // si on est en mode MANUEL et la fenêtre est OUVERTE
				$atlDiagnos = $atl->prepare('UPDATE status SET fenetre_ouvert = false');  // lorsqu'il y aura une update, la fenêtre se ferme
				$atlDiagnos->execute();
			if($atlState['auto_command']==false && $atlState['fenetre_ouvert']==false) // si on est en mode MANUEL et la fenêtre est FERME
				$atlDiagnos = $atl->prepare('UPDATE status SET fenetre_ouvert = true'); // lorsqu'il y aura une update, la fenêtre s'ouvre
				$atlDiagnos->execute();
		?>
		<?php
			}?>
		<?php header('location: gui.php');
		?>




		