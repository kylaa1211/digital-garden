# Changelog

## v0.3.0 - 2026-09-30

### Added
- Added an internal Go for a Stroll screen with a centered My Garden hub, radial branches, ambient circle nodes, direct panning, zoom controls, and an active Stroll button state.
- Added the Compost screen landscape with Paper-aligned cloud, flower, branch, terminal, tile, and modal styling.
- Added dark-mode and light-mode translucent button fills with backdrop blur.

### Changed
- Corrected app icon paths and assigned the available PNG assets across the Garden groups.
- Corrected app ordering and tree placement for the icon groups.
- Updated app popup labels to use the real icon names and brand capitalization.
- Added the Lucide shovel cursor for Compost while retaining scissors for pruning.
- Removed the garden flower-growth interruption and kept the Compost modal close action on the Compost screen.
- Matched the Garden toolbar corners and exposed the zoom/pan toolbar on Stroll.
- Updated the sun/moon control styling and centered the Garden ASCII flower.

### Deployment
- Local changes were kept staged during development and are being pushed in this release for GitHub/Vercel deployment.
