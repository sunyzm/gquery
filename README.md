# gquery

`gquery` provides a library and a simple CLI tool for querying geographic facts about world cities and airports.

## Installation

```bash
$ pip install git+https://github.com/sunyzm/gquery.git
```

## Usage

### CLI

```bash
$ gquery info "new york" "san francisco" london
$ gquery distance paris berlin
$ gquery distance "san francisco" "los angeles" --unit=mi
```

## License

`gquery` was created by tispell. It is licensed under the terms of the MIT license.

## Credits

Data sources:

- City data from https://simplemaps.com/data/world-cities
- Airport data from https://datacatalog.worldbank.org/search/dataset/0038117/Global-Airports
