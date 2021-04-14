OnwUI is swavan desktop application.

### How to build binary files
<ol>
    <li>
        <code>
        python setup.py py2app -A
        </code>
    </li>
    <li>
        <code>
         ./dist/SwaVanOneUI.app/Contents/MacOS/SwaVanOneUI
        </code>
    </li>
</ol>


### How to push the code in homebrew


### How to alter response body or headers
```
# Do not delete "swavan_response" method
# You can access response, headers, body and status using swavan
# You can add additional header i.e. swavan.response.headers["app_name"] = "swavan"

def swavan_response() -> None:
    # Add your logic here  
    swavan.response.body = b"apple" // Modified body
    swavan.response.headers["app_name"] // Modified headers
```
