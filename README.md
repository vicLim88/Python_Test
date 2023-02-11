# Test Automation with Pylenium on CakeDeFi
 
Prior to executing this test, please ensure that the following has been installed
1. pytest
2. pyleniumio

Command used to run all of the test
```ps1 Tab1
pytest
```
All of the tests will be executed.

Command used to run selected test
```ps1 Tab2
pytest -v -s -m sanity
```
Only test 'test_main_page_user_sees_logo' will be executed as it is marked with '@pytest.mark.sanity'
