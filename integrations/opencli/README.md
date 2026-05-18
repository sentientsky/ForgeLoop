# ForgeLoop OpenCLI Integration

This folder is an OpenCLI-compatible plugin source for ForgeLoop.

ForgeLoop integrates OpenCLI as an external peer dependency. OpenCLI is not copied into this repository.

Install the peer tool and this local plugin with:

```bash
python -m forgeloop opencli install . --execute
```

Preview first with:

```bash
python -m forgeloop opencli plan .
```

The plugin exposes read-only ForgeLoop commands through OpenCLI. It uses fixed subprocess arguments and does not use shell interpolation.

