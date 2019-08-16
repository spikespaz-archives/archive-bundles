# Project Archives (AKA "The Vault")

Archives of my old projects, mostly stored in Git bundles. This needs to exist because I start and abandon projects, but write too much code to throw away.

Every old project is packaged into a Git bundle file, in order to preserve history. To unpack these bundles, simply use the clone command. For example, `git clone ./spikespaz-old.project-name.bundle ./project-name` replacing `project-name` with an appropriate string.

---

## [dockypi](https://github.com/spikespaz/archives/raw/master/spikespaz-old.dockypi.bundle)

A fork of [RPi-Distro/pi-gen](https://github.com/RPi-Distro/pi-gen) intended to create a minimal build of Debian (Raspbian) preconfigured with Docker.

## [github-extended](https://github.com/spikespaz/archives/raw/master/spikespaz-old.github-extended.bundle)

The beginnings of a WebExtension for adding useful features to GitHub. Abandoned because features would be more appropriately submitted as patches to [Refined GitHub](https://github.com/sindresorhus/refined-github).

## [windows-tiledwm](https://github.com/spikespaz/archives/raw/master/spikespaz.windows-tiledwm.bundle)

Intended to bring the functionality tiling window managers from Linux into Windows. Window management functionality currently doesn't exist, the current source is a complete configuration file parser and global hotkey listener with something resembling an event system. Development halted due to a hitch with overriding system shortcuts that are no longer necessary. Solution would be to rewrite the hotkey listener as a low level keyboard hook.
