<!DOCTYPE html>
<html>
	<head>
		<meta http-equiv="refresh" content="5">
		<meta charset="utf-8" />
		<link rel="stylesheet" href="gui.css" />
		<title>Groupe 3 - GUI</title>
		<?php
		// on met la timezone sur le fuseau horaire de bruxelles, on défini les paramètres de connexion à la BD
		date_default_timezone_set('Europe/Brussels');
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
	</head>
	<header>
		<br/>
		<p class="digital">Derniere actualisation des donnees :   </p></td>
		<p class="digital"><?php
				//on se connecte à la base de données et on récupère les données
				$atlRequest = $atl->prepare('SELECT * FROM sensor_data WHERE id = (SELECT MAX(id) FROM sensor_data)');
				$atlRequest->execute();
				$atlContent = $atlRequest->fetchAll();?></p>
				<p class="digital"><?php foreach ($atlContent as $atlItem) {
				echo $atlItem['moment'].'   ';?>
				<?php
				}?></p></td> 
		<h1>Panneau de commande de la serre - Groupe 3</h1>
		<h2>Mortiaux Charles Emre Koc</h2>
		<br/>
	</header>
	<body>
		<table>
			<caption><h3>États des actionneurs</h3></caption>
			<tr>
				<td><p>Mode de pilotage</p></td>
				<td><p>Pompe</p></td>
				<td><p>Vérin</p></td>
			</tr>
			<tr>
				<td><p class="lien"><?php foreach ($atlStatus as $atlState) {
				if($atlState['auto_command']==true) // Si on clique sur le bouton sur lequel il est écrit "automatique" ou "manuel"
													// en fonction de l'état actuel du système, alors on modifie la valeur de auto_command dans la BD par
													// l'intermédiaire de switch_mode.php.Le système passe donc en automatique si il était en manuel ou
													// passe en mode manuel si il était en mode automatique.
					echo "<a href='switch_mode.php'>Automatique</a>";
				else
					echo "<a href='switch_mode.php'>Manuel</a>";?></p>
				<?php
				}?></td>
				<td><p class="lien"><?php foreach ($atlStatus as $atlState) {
				if($atlState['on_pompe']==true)// Si on clique sur le bouton sur lequel il est écrit "ON" ou "OFF"
												// en fonction de l'état actuel du système, alors on modifie la valeur de on_pompe dans la BD par
												// l'intermédiaire de on_off.php.La pompe est activée si elle ne l'était pas ou s'éteint si elle l'était activée. 
					echo "<a href='on_off.php'>ON</a>";
				else
					echo "<a href='on_off.php'>OFF</a>";?>
				<?php
				}?></p></td>
				<td><p class="lien"><?php foreach ($atlStatus as $atlState) {
				if($atlState['fenetre_ouvert']==true)// Si on clique sur le bouton sur lequel il est écrit "OUVERT" ou "FERME"
													 // en fonction de l'état actuel du système, alors on modifie la valeur de fenetre_ouvert dans la BD par
												     // l'intermédiaire de open_close.php. La fenêtre s'ouvre si elle ne l'était pas ou se ferme si elle était ouverte. 
					echo "<a href='open_close.php'>OUVERT</a>";
				else
					echo "<a href='open_close.php'>FERMÉ</a>";?>
				<?php
				}?></p></td>
			</tr>
		</table>
		</br>
		<table>
			<caption><h3>Données des capteurs</h3></caption>
			<tr>
				<td><p>Température intérieure</p></td>
				<td><p><?php foreach ($atlContent as $atlItem) { // mets à jour la valeur de la température intérieure à partir de la BD
				echo $atlItem['temp_int'].'°C';?> 
				<?php
				}?></p></td>
			</tr>
			<tr>
				<td><p>Hygrométrie</p></td>
				<td><p><?php foreach ($atlContent as $atlItem) { // mets à jour la valeur de l'humidité de l'air à partir de la BD
				echo $atlItem['humid_air'].'%';?>
				<?php
				}?></p></td>
			</tr>
			<tr>
				<td><p>Humidité</p></td>
				<td><p><?php foreach ($atlContent as $atlItem) {// mets à jour la valeur de l'humidité du sol à partir de la BD
				echo $atlItem['humid_sol'].'%';?>
				<?php
				}?></p></td>
			</tr>
			<tr>
				<td><p>Température extérieure</p></td>
				<td><p><?php foreach ($atlContent as $atlItem) {// mets à jour la valeur de la température extérieure à partir de la BD
				echo $atlItem['temp_ext'].'°C';?></p>
				<?php
				}?></p></td>
			</tr>
			<tr>
				<td><p>Inclinaison</p></td>
				<td><p><?php foreach ($atlContent as $atlItem) {// mets à jour la valeur de l'angle d'inclinaison de la fênetre à partir de la BD
				echo $atlItem['angle'].'°';?></p>
				<?php
				}?></td>
			</tr>
			<tr>
				<td><p>Luminosité</p></td>
				<td><p><?php foreach ($atlContent as $atlItem) {// mets à jour la valeur de la luminbosité à partir de la BD
				echo $atlItem['light'].' Lux';?></p>
				<?php
				}?></td>
			<tr>
				<td><p>Pluie</p></td>
				<td><p><?php foreach ($atlContent as $atlItem) {// mets à jour le booléen renseigant le fait qu'il pleuve ou non à partir de la BD
				if($atlItem['rain']==true)
					echo "Oui";
				else
					echo "Non";?></p>
				<?php
				}?></td>
		</table>
		<table>
			<caption><h3>INA</h3></caption>
			<tr>
				<td><p>Appareil</p></td>
				<td><p>Courant</p></td>
				<td><p>Tension</p></td>
				<td><p>Puissance</p></td>
			</tr>
			<tr>
				<td><p>Vérin</p></td>
				<td><p><?php foreach ($atlContent as $atlItem) { // mets à jour la valeur du courant qui passe dans le vérin à partir de la BD
				echo $atlItem['i_verin'].'A';?>
				<?php
				}?></p></td>
				<td><p><?php foreach ($atlContent as $atlItem) { // mets à jour la valeur de la tension aux bornes du vérin à partir de la BD
				echo $atlItem['v_verin'].'V';?>
				<?php
				}?></p></td>
				<td><p><?php foreach ($atlContent as $atlItem) { // mets à jour la valeur de la puissance consommée par le vérin à partir de la BD
				echo $atlItem['p_verin'].'W';?>
				<?php
				}?></p></td>
			</tr>
			<tr>
				<td><p>Pompe</p></td>
				<td><p><?php foreach ($atlContent as $atlItem) { // mets à jour la valeur du courant qui passe dans la pompe à partir de la BD
				echo $atlItem['i_pompe'].'A';?>
				<?php
				}?></p></td>
				<td><p><?php foreach ($atlContent as $atlItem) { // mets à jour la valeur de la tension aux bornes de la pompe à partir de la BD
				echo $atlItem['v_pompe'].'V';?></p>
				<?php
				}?></td>
				<td><p><?php foreach ($atlContent as $atlItem) { // mets à jour la valeur de la puissance consommée par la pompe à partir de la BD
				echo $atlItem['p_pompe'].'W';?>
				<?php
				}?></p></td>
			</tr>
			<tr>
				<td><p>Batterie</p></td>
				<td><p><?php foreach ($atlContent as $atlItem) { // mets à jour la valeur du courant qui passe dans la batterie à partir de la BD
				echo $atlItem['i_batt'].'A';?></p>
				<?php
				}?></p></td>
				<td><p><?php foreach ($atlContent as $atlItem) { // mets à jour la valeur de la tension aux bornes de la batterie à partir de la BD
				echo $atlItem['v_batt'].'V';?></p>
				<?php
				}?></p></td>
				<td><p><?php foreach ($atlContent as $atlItem) { // mets à jour la valeur de la puissance consommée par la batterie à partir de la BD
				echo $atlItem['p_batt'].'W';?>
				<?php
				}?></p></td>
			</tr>
			<tr>
				<td><p>Panneau solaire</p></td>
				<td><p><?php foreach ($atlContent as $atlItem) {// mets à jour la valeur du courant qui passe dans le panneau solaire à partir de la BD
				echo $atlItem['i_sp'].'A';?></p>
				<?php
				}?></p></td>
				<td><p><?php foreach ($atlContent as $atlItem) { // mets à jour la valeur de la tension aux bornes du panneau solaire à partir de la BD
				echo $atlItem['v_sp'].'V';?></p>
				<?php
				}?></p></td>
				<td><p><?php foreach ($atlContent as $atlItem) { // mets à jour la valeur de la puissance consommée par le panneau solaire à partir de la BD
				echo $atlItem['p_sp'].'W';?>
				<?php
				}?></p></td>
		</table>
	</body>
</html>
