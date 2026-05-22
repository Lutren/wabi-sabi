# Wabi-Sabi Adapters

This folder is the canonical local place for Wabi-Sabi adapter stubs and
provider placeholders.

Host-level launchers under `..\..\..\scripts` may call these files because
Windows startup shortcuts need a stable host entrypoint. The implementation
source belongs here, inside `apps/local/wabi-sabi`.

Do not store provider keys in this folder. Use environment variables or a local
secret store, and keep live network use behind Wabi-Sabi ActionGate.
