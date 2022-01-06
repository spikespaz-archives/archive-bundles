# Project Archives (AKA "The Vault")

This repository serves as an archive of my old projects, with commit history preserved in [Git Bundles][1].
This needs to exist because I start and abandon projects, but write too much code to throw away.
Some of these may be revived in the future if I have the spare time and drive required,
but feel free to have a go at working with the sources yourself.

You can download the bundle for each project by clicking the :package: icon, or browse the code online with the :open_file_folder: icon.

After downloading abundle, clone it to a path as if it were a normal repository.
```
git clone <bundle_path> <clone_path>
```
If you want to publish changes, create an empty repository on GitHub, change directory to the bundle's clone directory, and update the remote.
```
git remote set-url --push <your_repository>
```

---

## Projects

If there is no description for a project, click the :open_file_folder: icon to view the frozen contents of the project's main branch. There is often a `README` that contains either a description, some build information, or both.

### [:open_file_folder:][1000]&nbsp;[:package:][2000]&nbsp;&nbsp;spikespaz-old/dockypi

[1]: https://github.com/RPi-Distro/pi-gen
[2]: https://dietpi.com/

A fork of [RPi-Distro/pi-gen][1] pre-configured for a minimal docker environment. This was apandoned because there are better options available, such as [DietPi][2] (although I'm not sure they have an out-of-the-box environment for Docker).

---
### [:open_file_folder:][1001]&nbsp;[:package:][2001]&nbsp;&nbsp;spikespaz-old/ffbatcher

[3]: https://www.ffmpeg.org/

This is a simple tool for batch-processing media, converting from one format or container to another and preserving the directory structure by duplication. Under the hood it uses [`ffmpeg`][3], and the GUI is written with PyQt5. If I recall correctly, this application may be functional and perhaps even useful, albiet incomplete, and I recommend that whoever is interested in this should complete the existing code and send me an email or create an issue telling me where you're hosting your fork. I can put a link here for any passers-by.

---
### [:open_file_folder:][1002]&nbsp;[:package:][2002]&nbsp;&nbsp;spikespaz-old/github-extended

[4]: https://github.com/refined-github/refined-github
[5]: https://github.com/jasonlong/isometric-contributions

A WebExtension intended to add a useful-but-minimal set of features to GitHub, such as a download button for repository sub-directories. I wanted to make this as an alternative to the rather bloated [Refined GitHub][4] extension, but ended up using that anyway. I also recommend [Isometric Contributions][5] for some eye-candy.

---
### [:open_file_folder:][1003]&nbsp;[:package:][2003]&nbsp;&nbsp;spikespaz-old/js-games

No description yet. Try checking the browse directory for a README file.

---
### [:open_file_folder:][1004]&nbsp;[:package:][2004]&nbsp;&nbsp;spikespaz-old/litemeter

No description yet. Try checking the browse directory for a README file.

---
### [:open_file_folder:][1005]&nbsp;[:package:][2005]&nbsp;&nbsp;spikespaz-old/marker-qt

No description yet. Try checking the browse directory for a README file.

---
### [:open_file_folder:][1006]&nbsp;[:package:][2006]&nbsp;&nbsp;spikespaz-old/newstyle-widgets

No description yet. Try checking the browse directory for a README file.

---
### [:open_file_folder:][1007]&nbsp;[:package:][2007]&nbsp;&nbsp;spikespaz-old/pyqt-themes

No description yet. Try checking the browse directory for a README file.

---
### [:open_file_folder:][1008]&nbsp;[:package:][2008]&nbsp;&nbsp;spikespaz-old/python-ffpython

No description yet. Try checking the browse directory for a README file.

---
### [:open_file_folder:][1009]&nbsp;[:package:][2009]&nbsp;&nbsp;spikespaz-old/quizlet-py

No description yet. Try checking the browse directory for a README file.

---
### [:open_file_folder:][1010]&nbsp;[:package:][2010]&nbsp;&nbsp;spikespaz-old/raspi-composter

No description yet. Try checking the browse directory for a README file.

---
### [:open_file_folder:][1011]&nbsp;[:package:][2011]&nbsp;&nbsp;spikespaz-old/tools-js

No description yet. Try checking the browse directory for a README file.

---
### [:open_file_folder:][1012]&nbsp;[:package:][2012]&nbsp;&nbsp;spikespaz-old/vernier-py

No description yet. Try checking the browse directory for a README file.

---
### [:open_file_folder:][1013]&nbsp;[:package:][2013]&nbsp;&nbsp;spikespaz-old/website-legacy

No description yet. Try checking the browse directory for a README file.

---
### [:open_file_folder:][1014]&nbsp;[:package:][2014]&nbsp;&nbsp;spikespaz-old/windows-adwin

No description yet. Try checking the browse directory for a README file.

---
### [:open_file_folder:][1015]&nbsp;[:package:][2015]&nbsp;&nbsp;spikespaz/bonjour-installer

No description yet. Try checking the browse directory for a README file.

---
### [:open_file_folder:][1021]&nbsp;[:package:][2021]&nbsp;&nbsp;spikespaz/dawnlabs-carbon

[6]: https://github.com/carbon-app/carbon

A fork of [carbon-app/carbon][6] which adds a preset for Windows-10-style titlebar buttons. The addition is complete, but my pull-request was never merged as it was deemed to be outside of the interest of the project by the developers.

---
### [:open_file_folder:][1016]&nbsp;[:package:][2016]&nbsp;&nbsp;spikespaz/deconstruction-table-spigot

No description yet. Try checking the browse directory for a README file.

---
### [:open_file_folder:][1022]&nbsp;[:package:][2022]&nbsp;&nbsp;spikespaz/forge-radialmenu

[7]: https://github.com/spikespaz/modpack-builder/tree/master/modpack
[8]: https://github.com/spikespaz/modpack-builder

A Forge mod for Minecraft 1.12 that adds a radial menu that can be opened by holding a keybind. It was indented to allow any custom action to be added to this menu, and then perform the action corresponding with the angle of the mouse upon release. In the current state it can only execute Quark emotes and perform basic functions such as opening an inventory GUI. It probably contains some useful code for custom GUI rendering. I was building them in tandem with my [Quarantine Modpack][7] and [Modpack Builder][8] projects.

---
### [:open_file_folder:][1017]&nbsp;[:package:][2017]&nbsp;&nbsp;spikespaz/java-version-tool

No description yet. Try checking the browse directory for a README file.

---
### [:open_file_folder:][1018]&nbsp;[:package:][2018]&nbsp;&nbsp;spikespaz/public-3d-models

No description yet. Try checking the browse directory for a README file.

---
### [:open_file_folder:][1019]&nbsp;[:package:][2019]&nbsp;&nbsp;spikespaz/spikespaz-website

No description yet. Try checking the browse directory for a README file.

---
### [:open_file_folder:][1020]&nbsp;[:package:][2020]&nbsp;&nbsp;spikespaz/tool-scripts

No description yet. Try checking the browse directory for a README file.

---

[1]: https://git-scm.com/docs/git-bundle

[1000]: https://github.com/spikespaz/archives/tree/master/browse/spikespaz-old/dockypi
[1001]: https://github.com/spikespaz/archives/tree/master/browse/spikespaz-old/ffbatcher
[1002]: https://github.com/spikespaz/archives/tree/master/browse/spikespaz-old/github-extended
[1003]: https://github.com/spikespaz/archives/tree/master/browse/spikespaz-old/js-games
[1004]: https://github.com/spikespaz/archives/tree/master/browse/spikespaz-old/litemeter
[1005]: https://github.com/spikespaz/archives/tree/master/browse/spikespaz-old/marker-qt
[1006]: https://github.com/spikespaz/archives/tree/master/browse/spikespaz-old/newstyle-widgets
[1007]: https://github.com/spikespaz/archives/tree/master/browse/spikespaz-old/pyqt-themes
[1008]: https://github.com/spikespaz/archives/tree/master/browse/spikespaz-old/python-ffpython
[1009]: https://github.com/spikespaz/archives/tree/master/browse/spikespaz-old/quizlet-py
[1010]: https://github.com/spikespaz/archives/tree/master/browse/spikespaz-old/raspi-composter
[1011]: https://github.com/spikespaz/archives/tree/master/browse/spikespaz-old/tools-js
[1012]: https://github.com/spikespaz/archives/tree/master/browse/spikespaz-old/vernier-py
[1013]: https://github.com/spikespaz/archives/tree/master/browse/spikespaz-old/website-legacy
[1014]: https://github.com/spikespaz/archives/tree/master/browse/spikespaz-old/windows-adwin
[1015]: https://github.com/spikespaz/archives/tree/master/browse/spikespaz/bonjour-installer
[1016]: https://github.com/spikespaz/archives/tree/master/browse/spikespaz/deconstruction-table-spigot
[1017]: https://github.com/spikespaz/archives/tree/master/browse/spikespaz/java-version-tool
[1018]: https://github.com/spikespaz/archives/tree/master/browse/spikespaz/public-3d-models
[1019]: https://github.com/spikespaz/archives/tree/master/browse/spikespaz/spikespaz-website
[1020]: https://github.com/spikespaz/archives/tree/master/browse/spikespaz/tool-scripts
[1021]: https://github.com/spikespaz/archives/tree/master/browse/spikespaz/dawnlabs-carbon
[1022]: https://github.com/spikespaz/archives/tree/master/browse/spikespaz/forge-radialmenu

[2000]: https://github.com/spikespaz/archives/raw/master/bundle/spikespaz-old.dockypi.bundle
[2001]: https://github.com/spikespaz/archives/raw/master/bundle/spikespaz-old.ffbatcher.bundle
[2002]: https://github.com/spikespaz/archives/raw/master/bundle/spikespaz-old.github-extended.bundle
[2003]: https://github.com/spikespaz/archives/raw/master/bundle/spikespaz-old.js-games.bundle
[2004]: https://github.com/spikespaz/archives/raw/master/bundle/spikespaz-old.litemeter.bundle
[2005]: https://github.com/spikespaz/archives/raw/master/bundle/spikespaz-old.marker-qt.bundle
[2006]: https://github.com/spikespaz/archives/raw/master/bundle/spikespaz-old.newstyle-widgets.bundle
[2007]: https://github.com/spikespaz/archives/raw/master/bundle/spikespaz-old.pyqt-themes.bundle
[2008]: https://github.com/spikespaz/archives/raw/master/bundle/spikespaz-old.python-ffpython.bundle
[2009]: https://github.com/spikespaz/archives/raw/master/bundle/spikespaz-old.quizlet-py.bundle
[2010]: https://github.com/spikespaz/archives/raw/master/bundle/spikespaz-old.raspi-composter.bundle
[2011]: https://github.com/spikespaz/archives/raw/master/bundle/spikespaz-old.tools-js.bundle
[2012]: https://github.com/spikespaz/archives/raw/master/bundle/spikespaz-old.vernier-py.bundle
[2013]: https://github.com/spikespaz/archives/raw/master/bundle/spikespaz-old.website-legacy.bundle
[2014]: https://github.com/spikespaz/archives/raw/master/bundle/spikespaz-old.windows-adwin.bundle
[2015]: https://github.com/spikespaz/archives/raw/master/bundle/spikespaz.bonjour-installer.bundle
[2016]: https://github.com/spikespaz/archives/raw/master/bundle/spikespaz.deconstruction-table-spigot.bundle
[2017]: https://github.com/spikespaz/archives/raw/master/bundle/spikespaz.java-version-tool.bundle
[2018]: https://github.com/spikespaz/archives/raw/master/bundle/spikespaz.public-3d-models.bundle
[2019]: https://github.com/spikespaz/archives/raw/master/bundle/spikespaz.spikespaz-website.bundle
[2020]: https://github.com/spikespaz/archives/raw/master/bundle/spikespaz.tool-scripts.bundle
[2021]: https://github.com/spikespaz/archives/raw/master/bundle/spikespaz.dawnlabs-carbon.bundle
[2022]: https://github.com/spikespaz/archives/raw/master/bundle/spikespaz.spikespaz.forge-radialmenu.bundle
