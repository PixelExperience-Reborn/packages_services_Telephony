#!/usr/bin/env python3
"""Historical TeleService source checks; NO emergency/radio/Android17 test."""
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
A = "{http://schemas.android.com/apk/res/android}"


def check(ok, label):
    if not ok:
        raise AssertionError(label)
    print("PASS INVENTORY:", label)


def main():
    bp = (ROOT / "Android.bp").read_text()
    manifest = ET.parse(ROOT / "AndroidManifest.xml").getroot()
    check('name: "TeleService"' in bp and 'certificate: "platform"' in bp
          and 'privileged: true' in bp, "old privileged TeleService APK")
    check('"SettingsLibDefaults"' in bp and '"org.apache.http.legacy"' in bp,
          "archived UI defaults and legacy HTTP library")
    check('"org.apache.http.legacy.stubs.system"' not in bp
          and '"satellite-s2storage-ro"' not in bp,
          "old service lacks modern AOSP17 build dependencies")
    check(manifest.get("package") == "com.android.phone"
          and manifest.get(A + "sharedUserId") == "android.uid.phone",
          "system phone package / UID")
    radio = (ROOT / "src/com/android/phone/settings/RadioInfo.java").read_text()
    check((ROOT / "res/layout/radio_info.xml").exists()
          and "Theme.SubSettingsBase" in (ROOT / "AndroidManifest.xml").read_text(),
          "legacy PE RadioInfo theme adjustments present")
    config = (ROOT / "src/com/android/phone/CarrierConfigLoader.java").read_text()
    check("Build.VERSION.INCREMENTAL" in config,
          "historical carrier cache update detection present")
    check((ROOT / "assets/eri_311580.xml").is_file(),
          "archived US Cellular ERI config (not approved for mondrian)")
    check((ROOT / "TEST_MAPPING").is_file(),
          "historical telephony CTS/test mapping exists")
    print("PASS: historic source inventory only; AOSP17/modem/IMS/emergency NOT TESTED.")


if __name__ == "__main__":
    try:
        main()
    except (AssertionError, OSError, ET.ParseError) as exc:
        print("FAIL:", exc, file=sys.stderr)
        sys.exit(1)
