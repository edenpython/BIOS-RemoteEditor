Baidu-BIOS-RemoteEditor
==========================

  - For baidu test request, use `ipmitool` command remote control BMC.
  - Modify the bios setup item, ensure other item not be changed.
  - Parse the returned data according to the test case criteria to determine the test results is PASS or FAIL.

### Version
`Rev: 1.4.0`

### Usage

#### For more information

```bash
python RomoteDataCheck.py -- help
```

#### How to modify the data
  - You can modify the data in the `parameter.json` file
  - Modify the IPv4 or IPv6 host in the code.
  - Only need to modify the **value** and **host number(192.168.2.11)** don't remove any punctuation otherwise 
    caused syntax error.
    ```bash
    "intel": {
            "type": [0, 1, 2, 3, 4, 5, 6],
            "0": ["0xff", 0, 1, 2, 3, 4, 5, 6, 7],
            "1": ["0xff", 0, 1, 2, 3, 4, 5, 6],
            "2": ["0xff", 0, 1],
            "3": ["0xff", 0, 1, 2, 3, 4, 5],
            "4": ["0xff", 0],
            "5": ["0xff", 0, 1, 2, 3, 4, 5, 6, 7],
            "6": ["0xff", 0]
        }
        
    parser.add_option('-H', '--host',default='192.168.2.11',
                      dest='ip', action='store',
                      help='set remote IP ')
    group1 = OptionGroup(parser,
                         "Case1", 
                         "python {0} -H 192.168.2.11 ".format(script))

    ```

### Log

  - Check result in the terminal window

### Associates

  - Tester
    - Chen
    - Cheng

  - Developer
    - Shen.Eden
  
### Validation

  - `Intel`
     - Script has been vailidated by Chen at 2019-01-25.
  - `AMD`
     - Script has been vailidated by Cheng at 2019-03-19.

### Estimate

| **Operation** |  **Estimate**    |   **Qualification**    |
|:-------------:|:----------------:|:----------------------:|
|    Manual     |    `8 hours`     |   For manunal test     |
|    Script     |     `5 hours`    |   For script test      |

