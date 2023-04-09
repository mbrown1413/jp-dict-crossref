
# JP Grammar Dictionary Cross-reference Data

Given one entry in a grammar dictionary, this data will point you to the page
where the same entry occurs in another dictionary.

**View the data on [Google
Sheets](https://docs.google.com/spreadsheets/d/1sRvteCg5UdaLpMSheNZtNKhEZO7T1ZhtS7UoQSCq3bA/edit?usp=sharing)**,
or view the CSV files directly in this repository.

Each row represents an entry. The columns differ depending on the dictionary,
but the last few columns are always the page numbers which that entry appears
in other dictionaries.

Dictionaries covered:

* Dictionary of (Basic/Intermediate/Advanced) Japanese Grammar
    * Data: [`dojg.csv`](dojg.csv)
    * [Free online version](https://core6000.neocities.org/dojg/)
* A Handbook of Japanese Grammar Patterns
    * Data: [`hjgp.csv`](hjgp.csv)
    * [Free online version](https://core6000.neocities.org/hjgp/)
* A Dictionary of Japanese Particles
    * Data: [`dojp.csv`](dojp.csv)
    * [Free online version](https://archive.org/details/a-dictionary-of-japanese-particles/mode/2up)


## Development

The raw data from the `data/` folder is read to generate the csv files in the
root. See [data/README.md](data/README.md) for details on where the data came
from. For convenience, I'm committing the generated CSV files to the
repository, as well as updating the Google Sheet copy. I'll try to keep both up
to date when changes are made to the code.

To re-generate the CSV files, install beautifulsoup4 and run:

    $ python generate_csv.py

It's easy to edit `generate_csv.py` if you want to change the columns output.
Just keep in mind that most dictionaries implemented don't fill all of the data
fields.
