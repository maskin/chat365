# Renaming chat365 to pai

## Goal
Remove remaining references to "chat365" from the codebase to complete the renaming to "pai".

## User Review Required
> [!NOTE]
> `src/backend/chat365.db` appears to be an unused legacy database file, as the application is configured to use `pai.db`. It will be deleted.

## Proposed Changes

### Configuration
#### [MODIFY] [.gitignore](file:///Users/maskin/Library/CloudStorage/Dropbox/0.github/pai/.gitignore)
- Remove `chat365.db` entry.

### Backend
#### [DELETE] [chat365.db](file:///Users/maskin/Library/CloudStorage/Dropbox/0.github/pai/src/backend/chat365.db)
- Delete the unused database file.

## Verification Plan

### Automated Tests
- Run `grep` and `find` to ensure no "chat365" references remain.
- Verify the application still starts and connects to `pai.db`.

### Manual Verification
- Check `.gitignore` content.
- Confirm `src/backend/chat365.db` is gone.
