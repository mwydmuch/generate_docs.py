# `generate_docs.py`

`generate_docs.py` is a simple script for generating pdf/png/jpg files based on odf template file. Developed as a helper tool for ML in PL Virtual Event 2020 (https://virtual-event.mlinpl.org).

## Usage
```
Usage: generate_docs.py [OPTIONS]

Options:
  -t, --template_path TEXT    Path to ODT file with {} fields.  [required]
  -c, --content_path TEXT     Path to TSV or CSV file with data for the
                              template.  [required]

  -d, --delimiter TEXT        Delimiter for address book file.
                              [default: '\t']

  -o, --output_template TEXT  Output file path template. It should have odt,
                              pdf, png, or jpg extension.  [required]

  -k, --keep_odt              Keep odt instead of removing them after
                              conversion to the final file format.

  --help                      Show this message and exit.
```


python3 generate_docs.py -t certificates_template.odt -c content.csv -o "certificates/{filename}.pdf"