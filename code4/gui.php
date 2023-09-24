<!DOCTYPE html>
<html>
	<head>
		<meta http-equiv="refresh" content="5">  <!-- refresh la page toutes les 5s -->
		<meta charset="utf-8" />
		<link rel="stylesheet" href="gui.css" />
		<title>Groupe 1 - GUI</title>
		<?php
		date_default_timezone_set('Europe/Brussels');  // introduction du fuseau horaire pour la Belgique/ et paramètre de connexion à MySQL 
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
		<p class="digital">Derniere actualisation des donnees :   </p></td> <!-- change ma date/heure à chaque actualisation -->
		<p class="digital"><?php //connexion à la DB + récupération des données
				$atlRequest = $atl->prepare('SELECT * FROM sensor_data WHERE id = (SELECT MAX(id) FROM sensor_data)');
				$atlRequest->execute();
				$atlContent = $atlRequest->fetchAll();?></p>
				<p class="digital"><?php foreach ($atlContent as $atlItem) {
				echo $atlItem['moment'].'   ';?>
				<?php
				}?></p></td>
		<h1>Panneau de commande de la serre - Groupe 1</h1> <!-- "grand" titre -->
		<h2>Beirens Denis - Hardy Loïc - Thomas Thibault</h2> <!-- "moyen" titre -->
		<br/>
	</header>
	<body>
		<table>
			<caption><h3>États des actionneurs</h3></caption> <!-- titre du 1er tableau -->
			<tr>
				<td><p>Mode de pilotage</p></td>   <!-- nom de la 1er colonne, 1er ligne -->
				<td><p>Pompe</p></td> <!-- nom de la 2er colonne, 1er ligne dans "table"-->
				<td><p>Vérin</p></td>  <!-- nom de la 3er colonne, 1er ligne dans "table"-->
			</tr>
			<tr>
				<td><p class="lien"><?php foreach ($atlStatus as $atlState) {
				if($atlState['auto_command']==true) // Si on clique sur le bouton "MANUEL" ou "AUTOMATIQUE"
					// Par rapport à l'état du système :
					// la valeur de auto_command dans la dB est modifié par le script "switch_mode.php".
					// Si automatique -> on passe en manuel
					// Si manuel -> on passe en automatique
					echo "<a href='switch_mode.php'>Automatique</a>"; 
				else
					echo "<a href='switch_mode.php'>Manuel</a>";?></p>
				<?php 
				}?></td>
				<td><p class="lien"><?php foreach ($atlStatus as $atlState) { 
				if($atlState['on_pompe']==true) // Si on clique sur le bouton "ON" ou "OFF"
					// Par rapport à l'état du système :
					// la valeur de auto_command dans la dB est modifié par le script "on_off.php".
					// Si ON -> on passe en OFF
					// Si OFF -> on passe en ON
					echo "<a href='on_off.php'>ON</a>";  
				else
					echo "<a href='on_off.php'>OFF</a>";?> 
				<?php
				}?></p></td>
				<td><p class="lien"><?php foreach ($atlStatus as $atlState) { 
				if($atlState['fenetre_ouvert']==true)  // Si on clique sur le bouton "OUVERT" ou "FERMEE"
					// Par rapport à l'état du système :
					// la valeur de auto_command dans la dB est modifié par le script "open_close.php".
					// Si OUVERT -> on passe en FERMEE
					// Si FERMEE -> on passe en OUVERT
					echo "<a href='open_close.php'>OUVERT</a>";   
				else
					echo "<a href='open_close.php'>FERMe</a>";?> 
				<?php
				}?></p></td>
			</tr>
		</table>
		</br>
		<table>
			<caption><h3>Données des capteurs</h3></caption>
			<tr>
				<!-- Pour chacunes des valeurs, le procédé reste identique : -->
				<!-- on va toujours utiliser une boucle pour afficher les valeurs car celles-ci sont stockées dans un tuple (python) -->
				<!-- mets à jour les informations dans la DB -->
				<td><p>Température intérieure</p></td>
				<td><p><?php foreach ($atlContent as $atlItem) {
				echo $atlItem['temp_int'].'°C';?>
				<?php
				}?></p></td>
			</tr>
			<tr>
				<td><p>Hygrométrie</p></td>
				<td><p><?php foreach ($atlContent as $atlItem) {
				echo $atlItem['humid_air'].'%';?>
				<?php
				}?></p></td>
			</tr>
			<tr>
				<td><p>Humidité</p></td>
				<td><p><?php foreach ($atlContent as $atlItem) {
				echo $atlItem['humid_sol'].'%';?>
				<?php
				}?></p></td>
			</tr>
			<tr>
				<td><p>Température extérieure</p></td>
				<td><p><?php foreach ($atlContent as $atlItem) {
				echo $atlItem['temp_ext'].'°C';?></p>
				<?php
				}?></p></td>
			</tr>
			<tr>
				<td><p>Inclinaison</p></td>
				<td><p><?php foreach ($atlContent as $atlItem) {
				echo $atlItem['angle'].'°';?></p>
				<?php
				}?></td>
			</tr>
			<tr>
				<td><p>Luminosité</p></td>
				<td><p><?php foreach ($atlContent as $atlItem) {
				echo $atlItem['light'].' Lux';?></p>
				<?php
				}?></td>
			<tr>
				<td><p>Pluie</p></td>
				<td><p><?php foreach ($atlContent as $atlItem) {
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
				<td><p><?php foreach ($atlContent as $atlItem) {
				echo $atlItem['i_verin'].'A';?>
				<?php
				}?></p></td>
				<td><p><?php foreach ($atlContent as $atlItem) {
				echo $atlItem['v_verin'].'V';?>
				<?php
				}?></p></td>
				<td><p><?php foreach ($atlContent as $atlItem) {
				echo $atlItem['p_verin'].'W';?>
				<?php
				}?></p></td>
			</tr>
			<tr>
				<td><p>Pompe</p></td>
				<td><p><?php foreach ($atlContent as $atlItem) {
				echo $atlItem['i_pompe'].'A';?>
				<?php
				}?></p></td>
				<td><p><?php foreach ($atlContent as $atlItem) {
				echo $atlItem['v_pompe'].'V';?></p>
				<?php
				}?></td>
				<td><p><?php foreach ($atlContent as $atlItem) {
				echo $atlItem['p_pompe'].'W';?>
				<?php
				}?></p></td>
			</tr>
			<tr>
				<td><p>Batterie</p></td>
				<td><p><?php foreach ($atlContent as $atlItem) {
				echo $atlItem['i_batt'].'A';?></p>
				<?php
				}?></p></td>
				<td><p><?php foreach ($atlContent as $atlItem) {
				echo $atlItem['v_batt'].'V';?></p>
				<?php
				}?></p></td>
				<td><p><?php foreach ($atlContent as $atlItem) {
				echo $atlItem['p_batt'].'W';?>
				<?php
				}?></p></td>
			</tr>
			<tr>
				<td><p>Panneau solaire</p></td>
				<td><p><?php foreach ($atlContent as $atlItem) {
				echo $atlItem['i_sp'].'A';?></p>
				<?php
				}?></p></td>
				<td><p><?php foreach ($atlContent as $atlItem) {
				echo $atlItem['v_sp'].'V';?></p>
				<?php
				}?></p></td>
				<td><p><?php foreach ($atlContent as $atlItem) {
				echo $atlItem['p_sp'].'W';?>
				<?php
				}?></p></td>
		</table>
	</body>
</html>
