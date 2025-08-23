## Configuration

### Ranges (inclusive)

1. Q200 - Q300: units
2. Q301 - Q500: deposit types
3. Q501 - Q700 & Q10000 - Q11000: commodities
4. Q701 - Q800: epsg codes
5. Q1000 - Q1300: countries
6. Q1301 - Q1700: material forms
7. Q2001 - Q8000: states and provinces

### Sources of Mineral Sites

To access record of a source, users can provide a string specifying how to do it. The general format is: `<type>:::<url>` where in `<url>`, we support the following arguments:

- `{record_id}`: the record id of the mineral site
- `{page_number}`: the page number if the mineral

For each argument, we can provide a default value for it using this syntax: `{arg=value}`.

Available types are: `pdf`, `webpage`
