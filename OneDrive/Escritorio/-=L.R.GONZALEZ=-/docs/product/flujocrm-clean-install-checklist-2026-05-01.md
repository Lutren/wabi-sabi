# FlujoCRM Clean Install Checklist 2026-05-01

Status: `CLEAN_MACHINE_QA_READY / CURRENT_USER_QA_PASS / NOT_EXECUTED_ON_CLEAN_VM`

Target artifact:

- `apps\commercial\flujocrm\dist\FlujoCRM-Setup-1.0.0.exe`
- SHA256: `f7ffa5a513207b15f81778a1e524eff110ff0ea638b893d15e44cd8d88e513c1`
- Signature status: `NotSigned`

2026-05-02 note: this hash supersedes the earlier 2026-05-02 QA installer
after the installed UI fix. Current-user install/launch/uninstall QA passed; a
clean Windows VM/user pass is still pending. See
`docs/product/flujocrm-current-user-install-qa-2026-05-02.md`.

This checklist is for a clean Windows user or VM. Do not mark FlujoCRM ready for
sale until this checklist is executed and evidence is saved.

## Preflight

- [ ] Use a Windows machine or VM without the development repo.
- [ ] Copy only `FlujoCRM-Setup-1.0.0.exe` to the machine.
- [ ] Verify SHA256 before install.
- [ ] Confirm whether Windows SmartScreen or unknown-publisher warning appears.
- [ ] Capture screenshot of any warning shown to users.

## Install

- [ ] Run installer as a normal user first.
- [ ] Confirm install completes without admin-only assumptions.
- [ ] Confirm desktop/start-menu shortcuts if generated.
- [ ] Launch FlujoCRM from the installed app.
- [ ] Confirm the app opens the complete dashboard UI, not the historical
  placeholder page.
- [ ] Record installed version/path.

## App Smoke

- [ ] App window opens.
- [ ] Create a contact.
- [ ] Edit the contact.
- [ ] Create a pipeline item.
- [ ] Create a follow-up task.
- [ ] Close and reopen app.
- [ ] Confirm data persists.
- [ ] Confirm persistence occurs in SQLite:
  `%APPDATA%\FlujoCRM\data\flujocrm.db`.
- [ ] Confirm `stage`, `value` and `last_activity` columns exist after launch.
- [ ] Test CSV import with a tiny synthetic file.
- [ ] Test local backup/export if available in UI.

## Privacy / Support

- [ ] Confirm app does not require login.
- [ ] Confirm no cloud account is required.
- [ ] Confirm support copy points to `medioevo.saga@gmail.com` for pilot/MVP.
- [ ] Confirm no private MEDIOEVO/Claudio/RPG references appear in the app UI.

## Uninstall

- [ ] Uninstall from Windows settings.
- [ ] Confirm app executable is removed.
- [ ] Decide and document whether local user data remains intentionally.

## Evidence To Save

- Install result summary.
- Windows version.
- SHA256 verification result.
- Screenshot of unsigned warning or no warning.
- Screenshot of opened app with synthetic data.
- Notes on any failed step.

## Release Decision

After execution, classify:

- `PASS`: installer can be used for first paid pilot after legal/listing review.
- `REVIEW`: minor issues or warning copy needs adjustment.
- `BLOCK`: install, launch, persistence or privacy issue found.
