# Favicon Generator

### Usage

```
favicon_generator.py [-h] [-c CONFIG] [-s SVG]
                        [-ps PNG_SIZES [PNG_SIZES ...]]
                        [-is ICO_SIZES [ICO_SIZES ...]] [-pn PNG_NAME]
                        [-in ICO_NAME]

Generate favicons from an SVG.
```

### Optional Arguments

| Argument             | Parameters                  | Description                                                                      |
| ---------------------|---------------------------- | -------------------------------------------------------------------------------- |
| `-h`, `--help`       |                             | show this help message and exit                                                  |
| `-c`, `--config`     | `CONFIG`                    | Configuration file with settings to use instead of commands.                     |
| `-s`, `--svg` `SVG`  |                             | Input SVG path to generate icons from.                                           |
| `-ps`, `--png-sizes` | `PNG_SIZES [PNG_SIZES ...]` | List of sizes (by pixel width) to generate PNG icons for.                        |
| `-is`, `--ico-sizes` | `ICO_SIZES [ICO_SIZES ...]` | List of PNG icon sizes to embed in the ICO file. Merged with PNG sizes.          |
| `-pn`, `--png-name`  | `PNG_NAME`                  | Base filename to use for PNG files. Use '{}' as a variable placeholder for size. |
| `-in`, `--ico-name`  | `ICO_NAME`                  | Filename for the generated ICO output file.                                      |

## Example Config

```json
{
  "svg": "../MyIcon.svg",
  "png_sizes": [16, 32, 48, 64, 72, 96, 128, 196],
  "ico_sizes": [16, 32, 64, 128, 256],
  "png_name": "out/MyIcon-{}.png",
  "ico_name": "out/favicon.ico"
}
```
