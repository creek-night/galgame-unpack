# Third-party tools and source material

The repository contains original workflow instructions, wrappers and small adapters. It does not bundle game data, tool executables, GARbro DLLs, a game key database, WSL distributions, dependency wheels, or the maintainer's modified Hxv4 build tree.

| Component | Role | Source |
|---|---|---|
| Pillow | Image I/O and compositing | https://python-pillow.github.io/ |
| UnityPy | Unity serialization and asset decoding | https://github.com/K0lb3/UnityPy |
| python-soundfile / libsndfile | Optional audio decoding | https://github.com/bastibe/python-soundfile |
| NumPy | Optional audio sample validation | https://numpy.org/ |
| GARbro / GARbro Mod | Separately installed archive/image libraries | https://github.com/morkt/GARbro / https://github.com/crskycode/GARbro |

Install external dependencies from their maintainers and retain their own licenses/notices. The MIT license here covers this project's original work, not those packages or linked articles. `garbro_bridge.cs` calls separately installed public APIs; it does not embed the GARbro decoder implementation.

Format-specific references document the upstream implementation or author research used when selecting routes. The 129-page catalog preserves original links, author/maintainer attribution and applicability limits. Its summaries and proposed checks do not copy full articles or relicense the source material.

The Hxv4 wrapper accepts an externally supplied compatible decoder and manifest. The historical modified binary/source tree is not in this release; see the explicit [protocol and availability boundary](references/hxv4-tool-contract.md).
