Runkeeper's Health Graph is built for web apps.

If you're not a webapp, it's trickier to auth. Here's how:

Step 1) run example/auth_start_here.py
	This will print a url, paste this into your browser.
	After authorizing you'll be redirected to http://br3nda.com/?code=...
	Copy the value of the code variable to use in step 2

Step 2) run examples/auth_save_code.py <code>
	Pass the code from step1 on the command line.
	This will be used to finish authorisation, and token will be saved into a local sqlite database

Step 3) run examples/demo.py
	All other methods should work now that auth is complete. Running demo.py to check this.
