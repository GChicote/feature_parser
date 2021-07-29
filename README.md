# .feature parser

Parses .feature files to .e2e.js files for detox usage.

### How to use:
```sh
$ python3 feature_parser.py [.feature file]
```

### Example:
Being the input file 'USxxxAwesomeThing.feature':
```feature
Feature: An awesome new feature

    USxxx: Some cool user story

    Scenario: The feature works fine
    Given some precondition
    When the user touches a magic button
    Then incredible things happen

```

The output will be the 'USxxxAwesomeThing.e2e.js' file:
```javascript
/*
 * Author: Gabriel Chicote
 */

// Add corresponding import. Example:
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
