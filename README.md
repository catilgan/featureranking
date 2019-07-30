## Vagrant and Windows 10 VirtualBox VM

* URL: https://developer.microsoft.com/en-us/microsoft-edge/tools/vms/
* VM Login: Passw0rd!

## How to build the App on Win10

* Start the Cmder and enter following commands

```
$:> pushd \\VBOXSVR\FeatureRanking
$:> pipenv shell
$:> sh ./py2exe.sh
```

## TODO

### Text Datei:

- [ ] Formattierung für alle Ranking Methoden gleich gestalten
- [x] Für alle ausgewählte Ranking Methoden eine separate Datei (%filename%_%method%.txt)
- [ ] Tabelle mit Tabs
- [ ] Spalten: Name / Score

### Programm:

- [ ] Weitere Ranking Methoden implementieren (PCA, LASSO,..)
- [ ] Aufteilung der Resultate und Dateien pro Ranking Methode
- [ ] Fortschrittsanzeige der Berechnung -> Progress-Indikatoren,
- [ ] Fehlermeldungen- und Behandlung
- [ ] Fertige Implementation bis 7. Januar erwünscht; aber Tabelle und Paper haben Vorrang
- [ ] Bis Präsentation: Bugfixes und Installer für Windows 10

### Paper:

- [ ] Die Input und Output der Ranking Methoden/Algorithmen beschreiben
- [ ] Verweis auf die Implementationen
- [ ] Keinen grossen Aufwand für die Implementationsdetails
- [ ] Rankingsresultate -> Klassifizierung mit Features & Penalty -> Genauigkeit messen
