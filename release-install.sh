#! /usr/bin/env nix-shell
#!nix-shell -i bash -p androidenv.androidPkgs_9_0.platform-tools

adb -d uninstall org.ergvein.wallet
adb install -r ./android-release-apk/release/android-app-release.apk
