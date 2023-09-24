<!DOCTYPE html>
<html>
	<head>
		<meta http-equiv="refresh" content="5"> <!-- refresh la page toutes les 5s -->
		<meta charset="utf-8" />
		<link rel="stylesheet" href="gui.css" />
		<title>Groupe 1 - GUI</title>
		<?php
		date_default_timezone_set('Europe/Brussels'); // introduction du fuseau horraire pour la Belgique
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
		<p class="digital"><?php
				$atlRequest = $atl->prepare('SELECT * FROM sensor_data WHERE id = (SELECT MAX(id) FROM sensor_data)');
				$atlRequest->execute();
				$atlContent = $atlRequest->fetchAll();?></p>
				<p class="digital"><?php foreach ($atlContent as $atlItem) {
				echo $atlItem['moment'].'   ';?>
				<?php
				}?></p></td>
		<h1>Panneau de commande de la serre - Groupe 1</h1>  <!-- "grand" titre -->
		<h2>Beirens Denis - Hardy Loïc - Thomas Thibault</h2> <!-- "moyen" titre -->
		<br/>
	</header>
	<body>
		<table>
			<caption><h3>etats des actionneurs</h3></caption> <!-- titre du 1er tableau -->
			<tr>
				<td><p>Mode de pilotage</p></td>  <!-- nom de la 1er colonne, 1er ligne -->
				<td><p>Pompe</p></td> <!-- nom de la 2er colonne, 1er ligne dans "table"-->
				<td><p>Verin</p></td> <!-- nom de la 3er colonne, 1er ligne dans "table"-->
			</tr>
			<tr>
				<td><p class="lien"><?php foreach ($atlStatus as $atlState) { // Le boutton "MANUEL" est initiallement présent
				if($atlState['auto_command']==true)
					echo "<a href='switch_mode.php'>Automatique</a>"; // si la valeur devient "AUTOMATIQUE", alors le mode est automatique
				else
					echo "<a href='switch_mode.php'>Manuel</a>";?></p> <!-- sinon il est manuel -->
				<?php
				}?></td>
				<td><p class="lien"><?php foreach ($atlStatus as $atlState) { // Le boutton "OFF" est initiallement présent
				if($atlState['on_pompe']==true)
					echo "<a href='on_off.php'>ON</a>";  // si la valeur devient "ON", alors la pompe s'active
				else
					echo "<a href='on_off.php'>OFF</a>";?>  <!-- sinon elle s'éteint -->
				<?php
				}?></p></td>
				<td><p class="lien"><?php foreach ($atlStatus as $atlState) { // Le boutton "FERME" est initiallement présent
				if($atlState['fenetre_ouvert']==true)
					echo "<a href='open_close.php'>OUVERT</a>";   // si la valeur devient "OUVERT", alors le vérin s'active
				else
					echo "<a href='open_close.php'>FERMe</a>";?>   <!-- sinon il s'éteint -->
				<?php
				}?></p></td>
			</tr>
		</table>
		</br>
		<table>
			<caption><h3>Donnees des capteurs</h3></caption> <!-- titre du 2eme tableau -->
			<tr> 
				<!-- on va toujours utiliser une boucle pour afficher les valeurs car celles-ci sont stockées dans un tuple (python) -->
				<td><p>Temperature interieure</p></td>
				<td><p><?php foreach ($atlContent as $atlItem) {
				echo $atlItem['temp_int'].'°C';?>
				<?php
				}?></p></td>
				<td colspan="4"><p>INA</p></td>
			</tr>
			<tr>
				<td><p>Hygrometrie</p></td>
				<td><p><?php foreach ($atlContent as $atlItem) {
				echo $atlItem['humid_air'].'%';?>
				<?php
				}?></p></td>
				<td><p>Appareil</p></td>
				<td><p>Courant</p></td>
				<td><p>Tension</p></td>
				<td><p>Puissance</p></td>
			</tr>
			<tr>
				<td><p>Humidite</p></td>
				<td><p><?php foreach ($atlContent as $atlItem) {
				echo $atlItem['humid_sol'].'%';?>
				<?php
				}?></p></td>
				<td><p>Verin</p></td>
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
				<td><p>Temperature exterieure</p></td>
				<td><p><?php foreach ($atlContent as $atlItem) {
				echo $atlItem['temp_ext'].'°C';?></p>
				<?php
				}?></p></td>
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
				<td><p>Inclinaison</p></td>
				<td><p><?php foreach ($atlContent as $atlItem) {
				echo $atlItem['angle'].'°';?></p>
				<?php
				}?></td>
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
				<td><p>Luminosite</p></td>
				<td><p><?php foreach ($atlContent as $atlItem) {
				echo $atlItem['light'].'Lux';?></p>
				<?php
				}?></td>
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
