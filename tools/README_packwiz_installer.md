# The two vendored packwiz jars

`tools/` carries two jars on purpose.

| file | what it is |
|---|---|
| `packwiz-installer-bootstrap.jar` | the small launcher packwiz ships |
| `packwiz-installer.jar` | the actual installer, **pinned at v0.5.14** |

The three callers are `tools/check_pack_deps.py`, `tools/build_server.py` and
`tools/sync_instance.py` - CI, the server pack build, and the local dev-instance sync.

## Why the installer is vendored

The bootstrap exists to self-update the installer, and it does that by calling
`https://api.github.com/repos/comp500/packwiz-installer/releases/latest` **anonymously** on every
run. On a GitHub Actions runner, which shares an IP with the rest of the world, that gets rate
limited:

```
java.io.IOException: Server returned HTTP response code: 403 for URL:
  https://api.github.com/repos/comp500/packwiz-installer/releases/latest
2: packwiz-installer failed to resolve the pack's jars
```

A release drives that bootstrap **three times** in one run - the pinned-pack guard, the server pack
build, and the server mod-set guard - so it was three independent chances to fail the whole release.
It fired on PR CI on 2026-08-18 and again on PR #33 on 2026-08-20.

All three callers now pass `--bootstrap-no-update --bootstrap-main-jar <this jar>`, so **no GitHub API
call happens at all**. That fixes it locally as well as in CI, which a token or a cache would not.

## Bumping it

Rare, and only worth doing for a real fix - the installer is stable and the pack does not track it.

```sh
curl -fL -o tools/packwiz-installer.jar \
  https://github.com/packwiz/packwiz-installer/releases/download/vX.Y.Z/packwiz-installer.jar
```

`-f` matters: without it a typo'd version tag - the one field you have to edit - writes GitHub's
404 body to the jar path and exits 0, and you commit a few hundred bytes of HTML.

Then update the version in the table above, and run `python tools/check_pack_deps.py` - if the jar is
wrong or corrupt, resolution fails immediately and loudly rather than silently installing nothing.

**Do not restore the update check to get a newer installer.** That is the bug.

## These jars are not pack content

They live in `tools/`, never in `pack/`. The release workflow's no-jar assertion greps the built
CurseForge export, not the repo, so vendoring here does not trip it and is not a redistribution
concern - packwiz-installer is MIT.
