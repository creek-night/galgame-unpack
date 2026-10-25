# Third-party tools and source material

The repository contains original workflow instructions, wrappers and small adapters. It does not bundle game programs or media, tool executables, GARbro DLLs, WSL distributions, dependency wheels, or the maintainer's modified Hxv4 build tree.

| Component | Role | Source |
|---|---|---|
| Pillow | Image I/O and compositing | https://python-pillow.github.io/ |
| UnityPy | Unity serialization and asset decoding | https://github.com/K0lb3/UnityPy |
| python-soundfile / libsndfile | Optional audio decoding | https://github.com/bastibe/python-soundfile |
| NumPy | Optional audio sample validation | https://numpy.org/ |
| GARbro / GARbro Mod | Separately installed archive/image libraries | https://github.com/morkt/GARbro / https://github.com/crskycode/GARbro |

Install external dependencies from their maintainers and retain their own licenses/notices. The MIT license here covers this project's original work, not those packages or linked articles. `garbro_bridge.cs` calls separately installed public APIs; it does not embed the GARbro decoder implementation.

Format-specific references document the upstream implementation or author research used when selecting routes. The 251-page catalog preserves original links, author/maintainer attribution and applicability limits. Its summaries and proposed checks do not copy full articles or relicense the source material.

The Hxv4 wrapper accepts an externally supplied compatible decoder and manifest. The historical modified binary/source tree is not in this release; see the explicit [protocol and availability boundary](references/hxv4-tool-contract.md).

See [Disclaimer and privacy notice](DISCLAIMER.md) for third-party content rights, runtime limitations, and external-service data handling.

## Bundled ztj source records

The separate `references/ztjal/catalog.json` dataset contains edited article text from ztj at [乜都讲D](https://blog.ztjal.info/category/acg/acg-data), including historical commands, code examples and publicly documented resource parameters. It retains the articles' **CC BY-NC-SA 3.0** license; it is not MIT-licensed. Attribution, per-article links and editorial changes are preserved in the dataset and [NOTICE](references/ztjal/NOTICE.md). The original query script remains MIT-licensed. This dataset is separate from the 251-source summary catalog and overlaps it; the counts are not additive. The source author does not endorse this project.
