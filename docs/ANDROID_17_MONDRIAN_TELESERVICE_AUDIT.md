# P1 — TeleService / Android 17 / mondrian source audit

Date: 2026-11-04. **AUDIT ONLY — preserve official Android17 Telephony service and all original PE `seventeen` sources unchanged.**

## Provenance

- PixelExperience-Reborn historical `packages_services_Telephony` branch `seventeen` revision `862c17429a67d853f3e8bd12d4441fa97346bce2`. The source tree merged official Android14 r21 in `f76a9dc1e4a9266d19abfb49b04476b9acd6bbd1` (2024-01-30), with an old PE UI change at HEAD.
- Official AOSP17 r1 `platform/packages/services/Telephony`: commit `4a3830d926a5a84a6f5f7aab8d27e245e7880a68`, tree `301679ce600c4b4a9ae03667b9444d749dba7aad`. https://android.googlesource.com/platform/packages/services/Telephony/+/refs/tags/android-17.0.0_r1
- In the staged AOSP17 manifest the official path `packages/services/Telephony` is already present. Its adjacent source graph includes `packages/services/Telecomm`, `packages/modules/Telephony`, `packages/modules/Telecom` and `packages/providers/TelephonyProvider`.

## Verified Soong delta

The historical `Android.bp` creates privileged platform-signed `TeleService`, including the emergency dialer, and links `telephony-common`, `voip-common`, `ims-common` and `org.apache.http.legacy`. It contains `defaults: ["SettingsLibDefaults"]` from a PE-specific RadioInfo UI adaptation.

Official AOSP17 `Android.bp` still builds `TeleService` but uses `org.apache.http.legacy.stubs.system`, `modules-utils-fastxmlserializer`, `android.permission.flags-aconfig-java-export`, `satellite-s2storage-ro`, `s2-geometry-library-java`, `dropbox_flags_lib`, `generate_product_characteristics_rro: true`, and the official framework shared sources. It does not carry the historical blanket `SettingsLibDefaults` from PE. This is an interconnected Android17 framework/IMS/satellite/RIL build graph, not a theme-only file replacement.

Official source: https://android.googlesource.com/platform/packages/services/Telephony/+/refs/tags/android-17.0.0_r1/Android.bp

## Historical changes, evidence and decision

| Commit | Old change | Treatment |
| --- | --- | --- |
| `862c17429a67d853f3e8bd12d4441fa97346bce2` | "Telephony: Adapt to S style": `SettingsLibDefaults`, RadioInfo layout/buttons/style, `Theme.SubSettingsBase` | **UI-only candidate** after Android17 theme resource and UI tests; do **not** replace entire Android17 TeleService or introduce an obsolete SettingsLib dependency. |
| `52d20f5616a3dd8d392734934df20c4b2e518ac4` | CarrierConfigLoader update detection changes from `Build.FINGERPRINT` to `Build.VERSION.INCREMENTAL` | **DEFER**: verify newer AOSP17 cache invalidation, SIM/carrier config, OTA and downgrade behavior first. An incremental value alone is not proof that vendor/telephony configs are unchanged. |
| `3f3701eb96fb1d23d8ef9596b3c8d29eb24587a4` | U.S. Cellular-specific ERI XML | **OUT OF SCOPE** for mondrian initial PE-Reborn product unless a concrete tested carrier demand exists; importing broad carrier overrides is not safe. |
| `5d2e2b324ad431b7daca1680949f30fda6cc3ff4` | Mark `enhanced_4g_lte_mode_title_variant` as untranslatable | **REVIEW** current Android17 resource/translation rules and carrier config, not a reason to replace TeleService. |
| `66840a93b6b6e2e2d849b94daeab8d03d8f8acfd` | Android14-era **DO NOT MERGE** emergency SIM selection and normal-routing change touching `ecc` database/tests | **BLOCKED** pending current AOSP17 emergency routing and modem tests. Its existence in historical history does not prove an unported PE feature. **Do not cherry-pick** into the clean AOSP17 product. |

## Device / release risk gates

1. For the independent PE-Reborn Android17 mondrian tree, verify RIL/AIDL, IMS MMTEL, radio registration, correct carrier overlays, phone/SMS/data, VoLTE, emergency calling and carrier config on actual hardware. Current LF52406 LineageOS-derived trees are hardware *references only*.
2. Never relax `MODIFY_PHONE_STATE`, emergency phone-call permissions, IMS, SMS or carrier privileges to make an old Settings theme work.
3. Use the upstream Android17 `TeleService` with matching `packages/modules/Telephony` and `Telecomm` graph; test all runtime flags, `platform` signing and privapp permissions.
4. Run TeleServiceTests, CTS telephony/emergency/IMS suites as appropriate, carrier config tests, default dialer/role behavior, multi-user boundaries, subscription updates, dual-SIM if supported, airplane mode and reboot persistence.
5. Full Android17 build and actual mondrian modem/emergency behavior are **NOT** yet tested.

## Status

- [x] Historical PE and AOSP17 exact revision provenance identified.
- [x] Historical UI/carrier/emergency commits inventoried, with explicit non-port decisions.
- [x] Host-only source inventory CI created.
- [ ] Full historical non-upstream commit-by-commit review and current API equivalence.
- [ ] Targeted official AOSP17 exact-source sync and Soong compile.
- [ ] Independent PE-Reborn mondrian device product, RIL/IMS/eUICC/CarrierConfig/CTS tests.

**Decision:** keep the official Android17 Telephony service. Audit only; do not add or replace old `seventeen` implementation in manifest.
