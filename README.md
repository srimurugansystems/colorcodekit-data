# colorcodekit-data

The 148 CSS named colors as a CSV and a JSON file, with the codes most projects need and two computed fields that are hard to find elsewhere: the best text color for each color, and its nearest other named color.

Public domain (CC0 1.0). Version 2026-11-17. Published with the [Open Color Data page on colorcodekit.com](https://colorcodekit.com/open-data/).

## Files

| File | What it is |
| --- | --- |
| `data/css-named-colors.csv` | One row per named color, 148 rows, 20 columns |
| `data/css-named-colors.json` | The same rows plus metadata (version, license, source) |
| `datapackage.json` | [Data Package](https://datapackage.org/) description of the CSV, for tools that read it |
| `scripts/verify.py` | Standard-library check that the files are consistent (run it after any edit) |
| `LICENSE` | CC0 1.0 Universal legal text |
| `CITATION.cff` | How to cite |

## Columns

| Column | Type | Meaning |
| --- | --- | --- |
| `name` | text | The CSS keyword, lowercase. |
| `hex` | text | Six-digit hex code, uppercase, with #. |
| `r, g, b` | integer | sRGB channels, 0 to 255. |
| `hsl_h, hsl_s, hsl_l` | integer | HSL as degrees, percent and percent, rounded. |
| `oklch_l, oklch_c, oklch_h` | number | OKLCH lightness (0 to 1), chroma and hue in degrees. Hue is 0 for grays. |
| `cmyk_c, cmyk_m, cmyk_y, cmyk_k` | integer | A direct screen conversion in percent. It is not a print profile. |
| `best_text` | text | #FFFFFF or #000000, whichever has the higher WCAG contrast on this color. |
| `best_text_contrast` | number | The WCAG 2.2 contrast ratio of that text color on this color. |
| `same_hex_as` | text | Other keywords with the same value, separated by semicolons. For example aqua and cyan. |
| `nearest_other` | text | The closest other named color with a different hex, by CIEDE2000. |
| `nearest_other_deltaE2000` | number | That distance. Below 1 is hard to see. Above about 5 the colors read as different. |

## Use it

```python
import pandas as pd

df = pd.read_csv("data/css-named-colors.csv")
print(df[df.best_text == "#FFFFFF"].head())
```

```js
const { colors } = await (await fetch("https://raw.githubusercontent.com/srimurugansystems/colorcodekit-data/main/data/css-named-colors.json")).json();
const darks = colors.filter(c => c.best_text === "#FFFFFF");
```

## Method and source

- Names and RGB values come from [section 6.1 of the W3C CSS Color Module Level 4](https://www.w3.org/TR/css-color-4/#named-colors).
- HSL uses the standard sRGB conversion. OKLCH uses the matrices published by Bjorn Ottosson. Contrast follows the WCAG 2.2 relative luminance formula.
- The nearest other color is the smallest CIEDE2000 distance (Sharma, Wu and Dalal, 2005) to a named color with a different hex.
- CMYK is a plain screen conversion in percent. It is not a print profile and will not match printed color.

Everything computed here is reproducible from the names and RGB values. `scripts/verify.py` recomputes the hex and RGB agreement and checks the row counts.

## License

CC0 1.0 Universal. Use, change and redistribute it for any purpose with no permission needed. A link back is welcome and not required.

## Cite

Colorcodekit.com, "CSS named colors dataset", version 2026-11-17, https://colorcodekit.com/open-data/, CC0 1.0.

## Corrections

Found a wrong value? Open an issue with the color name and the value you expected, and a source for it.
