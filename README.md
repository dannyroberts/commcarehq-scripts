# Get domain admin emails for a list of domains

## Create your input file

1. Put the domains together in a file, one domain name per line.
   Make sure that the file ends in a newline.
   (Do not use Word or a rich text editor.)
2. Save it as domain-list.txt

## Get your logged-in CommCare HQ sessionid cookie:

1. Go to your browser and open developer tools
2. Navigate to www.commcarehq.org
  - (Log in if you aren't logged in)
3. Inspect the request and take note of the value of the `sessionid` cookie

## Clone this gist to your computer

```bash
git clone https://gist.github.com/1942d2cd9a9cb0b8cf27.git pull-domain-admins
cd pull-domain-admins
```

## Run the script

Move domain-list.txt from above into the pull-domain-admins directory.

(Tip: On Mac you can run `open .` to open the current directory
in the Finder)

Then run

```
bash pull-domain-admins.sh ${commcarehq-sessionid-cookie} < domain-list.txt | tee domain-admins.txt
```

but replace `${commcarehq-sessionid-cookie}` with your `sessionid` from above.

## Result

The admin email should now be listed in `domain-admins.txt`, one line per domain.
