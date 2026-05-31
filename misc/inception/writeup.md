The general idea for this challenge is that the file in question is a Polyglot file (https://en.wikipedia.org/wiki/Polyglot_(computing)). This means that the file is technically multiple different file types, that are all valid and can be parsed correctly. In this case, the challenge file is simultaniously a .png, a .zip, and a .pdf file. 

## Step 1

To start, the file has no extention and no instructions. The first move on any unknown file is to run `file` and `strings`:

```bash
$ file inception 
inception: PNG image data, 273 x 160, 8-bit/color RGB, non-interlaced
```

It's a PNG. Open it in any image viewer and you'll find part one of the flag.
 
`strings` won't reveal much — the interesting content has been stripped or compressed — but a more thorough recon tool will:
 
```bash
$ binwalk inception_challenge.bin
 
DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
0             0x0             PNG image, 525 x 160, 8-bit/color RGB, non-interlaced
1187          0x4A3           Zip archive data, at least v2.0 to extract
1483          0x5CB           End of Zip archive
1561          0x619           PDF document, version 1.4
```

At this point its clear that there are some strange things happening in the file. The file reports a PNG, a Zip archive, and a PDF. 

## Step 2 — Extract the ZIP
 
ZIP archives store their directory index at the *end* of the file, so `unzip` can read the archive even with a PNG prepended to it.
 
```bash
$ unzip inception_challenge.bin
Archive:  inception_challenge.bin
warning [inception_challenge.bin]:  1187 extra bytes at beginning or within zipfile
  (attempting to process anyway)
  inflating: data.bin
 
$ cat data.bin
```

This gives you part two of the flag.

## Step 3 — Extract the PDF
 
PDF readers scan *backwards* from the end of a file looking for `%%EOF`, so the PDF is valid despite being appended after the PNG and ZIP data. Open it in any PDF viewer, or extract the text directly:
 
```bash
$ pdftotext inception_challenge.bin -
```

This gives you part three of the flag.

Flag: byuctf{wh4t_th3_fr3ak}

