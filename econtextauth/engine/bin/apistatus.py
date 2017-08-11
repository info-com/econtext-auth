"""
A simple healthcheck to see if the eContext site is up and running.  This should
be run from Cron periodically to check on the status of the API server which
calls out to /v2/status and checks for a 200, or other error and sends a push
notification via Pushover to the API distribution group.

Also, since we *do* have a wait time built into this script, you should probably
shelter the cron job behind flock or something so that this script doesn't get
called multiple times.

*/5 * * * * /usr/bin/flock -n /tmp/api-status.lock /usr/local/bin/econtext-api-status -vvv ... &>> /var/log/econtext/api-status.log
*/5 * * * * /usr/bin/flock -n /tmp/api-inhouse-status.lock /usr/local/bin/econtext-api-status -vvv --host api-inhouse.econtext.com ... &>> /var/log/econtext/api-status.log
"""

import requests
import logging
import time
import json

log = logging.getLogger('econtext')


def init_logging(verbose=0, name=u"econtext", *args, **kwargs):
    log = logging.getLogger(name)
    verbosity = logging.ERROR
    if verbose is not None and verbose >= 1:
        verbosity = logging.INFO
    if verbose is not None and verbose >= 2:
        verbosity = logging.DEBUG
    
    log.setLevel(verbosity)
    h = logging.StreamHandler()
    h.setFormatter(logging.Formatter(u"%(process)s - %(asctime)s - %(levelname)s :: %(message)s", u"%Y-%m-%d %H:%M:%S"))
    log.addHandler(h)
    h.setLevel(verbosity)
    return log


def main():
    import argparse
    
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-v", "--verbose", dest="verbose", default=0, action="count", help="Be verbose")
    parser.add_argument("--host", dest="host", default="auth.econtext.ai", help="Host name to check")
    parser.add_argument("--eu", dest="eu", default=None, help="eContext Auth API user")
    parser.add_argument("--ep", dest="ep", default=None, help="eContext Auth API password")
    parser.add_argument("--pa", dest="pa", default=None, help="Pushover App token")
    parser.add_argument("--pu", dest="pu", default=None, help="Pushover User key")
    parser.add_argument("--sleep", dest="sleep", default=3600, help="If there is an error, wait this long before checking again", metavar="SEC")
    options = parser.parse_args()
    log = init_logging(options.verbose)
    
    sleep = options.sleep
    eu = options.eu
    ep = options.ep
    pa = options.pa
    pu = options.pu
    if eu is None or ep is None or pa is None or pu is None:
        raise Exception("An error occurred - missing credentials")
    
    host = options.host
    url = "https://{}/api/status".format(host)
    log.debug("Checking status from {}".format(url))
    response = requests.get(url, auth=requests.auth.HTTPBasicAuth(eu, ep))
    if response.status_code == 200:
        log.debug("Status is 200")
        return
    
    log.warn("Status is {}".format(response.status_code))
    # If there was an error - lets send a notice about it
    # Also, because I don't want to get inundated with errors, after we send an
    # error, it's okay to sleep for a while!
    title = "Problem with {}".format(host)
    message = "There was an error"
    result = "There was an error"
    
    try:
        result = response.json()
        message = result['econtext']['traceback']
    except:
        pass
    
    log.error("{}: {}".format(title, message))
    log.error("Full result: {}".format(json.dumps(result)))
    
    data = {"token": pa, "user": pu, "title": title, "message": message, "priority": 0}
    if host == "auth.econtext.ai":
        # Lambda should take care of the "repeat" stuff...
        data['priority'] = 2  # priority of 1 (interrupt me)
        data['retry'] = 30  # retry every 30 seconds
        data['expire'] = sleep  # expire after an hour (this is how long we should sleep)
    
    response = requests.post("https://api.pushover.net/1/messages.json", data=data)
    log.debug("Pushover message delivered")
    log.debug("Pushover response: {}".format(response.text))
    log.debug("Waiting for {} seconds before checking again".format(sleep))
    time.sleep(sleep)
    log.debug("Wait completed - exiting...")
    return


if __name__ == "__main__":
    main()



