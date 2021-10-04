# .feature parser

Parses .feature files to .e2e.js files for detox usage.

## How to use:

---

### Parsing an arbitrary number of files
By default, you can pass an arbitrary number files paths and they will be parsed.
```sh
python3 feature_parser.py <abs_path_1>/dir1/file1.feature <abs_path_2>/dir2/file2.feature ...
```
The new files will be saved inside the `step_definitions/` directory, which will be created inside the directory containing the first file passed to the program.
So in this case, all output files will be saved inside `<abs_path_1>/dir1/setp_definitions/`

---

### Parsing all files inside a directory
If you want to, you can tell it to parse all files inside a given directory passing it the `-d` flag.

```sh
python3 feature_parser.py -d <abs_path>/dir/
```

Here, all .feature files inside `<abs_path>/dir` will be parsed and the resulting files will be saved inside `<abs_path>/dir/step_definitions`

---

### Help

You can always run the program with the help flag for more information.
```sh
python3 feature_parser.py -h
```

```sh
usage: feature_parser.py [-h] [-d] [-V] path [path ...]

Parse files from [.feature] format into [.e2e.js] format

positional arguments:
  path           Path to work with

optional arguments:
  -h, --help     show this help message and exit
  -d, --dir      parses all files in specified directory
  -V, --version  shows CLI version
```

---

## Example:
Being the input file 'USxxxAwesomeThing.feature':
```feature
Feature: An awesome new feature

    USxxx: Some cool user story

    Scenario: The feature works fine
      Given some precondition
      When the user touches a magic button
      Then incredible things happen

```

Running
```sh
python3 feature_parser.py USxxxAwesomeThing.feature
```

will create the following file inside the `step_definitions` directory.
Note that this directory will be created if it doesn't exist.

The output will be the 'USxxxAwesomeThing.e2e.js' file:
```javascript
/**
 * Author: Gabriel Chicote
 */

// Add corresponding imports. For example:
import { describe } from 'jest-circus';

describe( 'USxxx - An awesome new feature', () => {

	beforeAll( () => {
		await device.launchApp();
	} );

	beforeEach( () => {
		await device.reloadReactNative();
	} );


    describe( 'The feature works fine', () => { 

        const given = 'Given some precondition'
        const when = 'When the user touches a magic button'
        const then = 'Then incredible things happen'

        test( `${given}, ${when} ${then}`, async () => { 
            // TODO
        })

    } ); 
    
});
```
