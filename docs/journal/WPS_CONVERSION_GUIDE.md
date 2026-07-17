# Converting .wps Journal Files

The weekly journal entries (Journal Week 1.wps through Journal Week 10.wps) are in **Microsoft Works** (.wps) binary format from 2004. This format is no longer supported by modern software, so they need to be converted before the content can be read and pasted into the markdown files in `docs/journal/weeks/`.

---

## Option 1: Microsoft Works 6-9 File Converter (Windows)

Microsoft released a free converter that lets Word open .wps files.

1. Download "Microsoft Works 6-9 File Converter" (search for `WorksConv.exe` — it may still be available from archive sites)
2. Install it on Windows
3. Open Microsoft Word
4. File → Open → change file type filter to "Works 6-9 (*.wps)"
5. Select the .wps file
6. Copy the text content
7. Paste into the corresponding `docs/journal/weeks/week-XX.md` file

## Option 2: Coolutils Online Converter

A free online tool that converts .wps to .doc or .pdf.

1. Go to [https://www.coolutils.com/online/WPS-to-DOC](https://www.coolutils.com/online/WPS-to-DOC)
2. Upload the .wps file
3. Choose output format (DOC or TXT recommended)
4. Download the converted file
5. Copy the text content into the corresponding markdown file

## Option 3: LibreOffice

Some versions of LibreOffice can open .wps files directly.

1. Download LibreOffice from [https://www.libreoffice.org](https://www.libreoffice.org)
2. Open LibreOffice Writer
3. File → Open → select the .wps file
4. If it opens successfully, select all text and copy
5. Paste into the markdown file

## Option 4: Zamzar Online Converter

Another online conversion service.

1. Go to [https://www.zamzar.com](https://www.zamzar.com)
2. Upload the .wps file
3. Convert to .txt or .doc
4. Download and copy content

---

## Where Are the .wps Files?

The original .wps files are NOT in this Git repository (they're excluded by `.gitignore`). You'll need to find them from your original backup. The files were:

- `Journal Week 1.wps`
- `Journal Week 2.wps`
- `Journal Week 3.wps`
- `Journal Week 4.wps`
- `Journal Week 5.wps`
- `Journal Week 6.wps`
- `Journal Week 7.wps`
- `Journal Week 8.wps`
- `Journal Week 9.wps`
- `Journal Week 10.wps`

They were originally located in the `Modeling Motion/` directory of the repo before reorganization.

---

## After Conversion

Once you have the text content:

1. Open the corresponding `docs/journal/weeks/week-XX.md` file
2. Replace the "Content pending conversion" placeholder section with the actual journal text
3. Update the `status` in the YAML front matter from `pending_conversion` to `converted`
4. Add any relevant cross-references to code files mentioned in the entry
5. Commit the changes
