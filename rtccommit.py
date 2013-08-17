import subprocess
import re
import os

# RTC commit works in 5 steps:
# (1) Login
# (2) Check in any changes
# (3) Update the checked in changeset (mainly by adding comments)
# (4) Deliver the changes
# (5) Logout
def rtc_commit(username, password, dir, comment='Committing changes', repoURL='https://rtp-rtc17.tivlab.raleigh.ibm.com:9443/jazz', changesetID="", workspace="", scmfile=""):
    if not username:
        print "Please enter a username."
        return 0
    elif not password:
        print "Please enter a password."
        return 0
    elif not dir:
        print "Please enter the directory to commit."
        return 0
    elif not os.path.isdir(dir):
        print "The directory '" + dir + "' does not exist. Please enter a valid directory."
        return 0
    
    # Find the RTC command line executable.
    if not scmfile:
        try:
            programFilesDir = os.environ['PROGRAMFILES(X86)']
        except:
            try:
                programFilesDir = os.environ['PROGRAMFILES']
            except:
                programFilesDir = "C:\Program Files"
        scmfile = programFilesDir + '/IBM/TeamConcert/scmtools/eclipse/scm.exe'
    
    if os.path.isfile(scmfile):
        # Login
        print "Logging into RTC."
        login = subprocess.Popen([scmfile, 'login', '-r', repoURL, '-u', username, '-P', password], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        loginout, loginerr = login.communicate()
        if loginerr:
            print "Error logging in: " + loginerr
            return 0
        elif loginout:
            print loginout

        if not changesetID:
            # Check in the changes
            print "Checking in any changes."
            checkin = subprocess.Popen([scmfile, 'checkin', '-u', username, '-P', password, dir], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            checkinout, checkinerr = checkin.communicate()
            if checkinerr:
                print "Error checking in directory '" + dir + "': " + checkinerr
                rtc_logout(scmfile, repoURL)
                return 0
            # If successfully checked in items, update the changelist by adding comment
            elif checkinout:
                print checkinout

                searchObj = re.search(r'\n\s+Change sets:\s*\((\d+)\)', checkinout, re.DOTALL)
                if searchObj:
                    try:
                        changesetID = searchObj.group(1)
                    except:
                        print "Can't grab changeset ID from previous output. This is bad since items have been checked in."
                        rtc_logout(scmfile, repoURL)
                        return 0
                else:
                    print "Can't grab changeset ID from previous output. This is bad since items have been checked in."
                    rtc_logout(scmfile, repoURL)
                    return 0
                    
                print "Adding a comment to changeset#" + changesetID + "."
                changeset = subprocess.Popen([scmfile, 'changeset', 'comment', '-u', username, '-P', password, changesetID, comment], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                changesetout, changeseterr = changeset.communicate()
                if changeseterr:
                    print "Error writing comment to changeset#" + changesetID +": " + changeseterr
                    rtc_logout(scmfile, repoURL)
                    return 0
                elif changesetout:
                    print changesetout
            # If nothing was checked in, then we should just move directly to "deliver/commit"
            else:
                print "Nothing was checked in. Perhaps a previous changeset was already checked in. Will try to deliver any outstanding changesets."
        else:
            # Changeset ID provided, so will do target changeset delivery
            print "Changeset ID provided. Will just deliver/commit that particular changeset."
        
        # Deliver/commit the changes
        if changesetID:
            print "Delivering/committing any changes via changeset ID " + changesetID + "."
            deliver = subprocess.Popen([scmfile, 'deliver', '-u', username, '-P', password, '-d', dir, '-c', changesetID], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        elif workspace:
            print "Delivering/committing any changes via workspace name " + workspace + "."
            deliver = subprocess.Popen([scmfile, 'deliver', '-u', username, '-P', password, '-d', dir, '-s', workspace], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:
            print "Delivering/committing any changes."
            deliver = subprocess.Popen([scmfile, 'deliver', '-u', username, '-P', password, '-d', dir], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        deliverout, delivererr = deliver.communicate()
        if deliverout:
            print deliverout
        if delivererr:
            print "Error delivering (committing) changes: " + delivererr

        # Log out
        rtc_logout(scmfile, repoURL)
    else:
        print "Error committing to RTC: can't find RTC executable file: " + scmfile
        return 0
    return 1

def rtc_logout(scmfile, repoURL='https://rtp-rtc17.tivlab.raleigh.ibm.com:9443/jazz'):
    if not scmfile:
        try:
            programFilesDir = os.environ['PROGRAMFILES(X86)']
        except:
            try:
                programFilesDir = os.environ['PROGRAMFILES']
            except:
                programFilesDir = "C:\Program Files"
        scmfile = programFilesDir + '/IBM/TeamConcert/scmtools/eclipse/scm.exe'
        
    if os.path.isfile(scmfile):
        print "Logging out of RTC."
        logout = subprocess.Popen([scmfile, 'logout', '-r', repoURL], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        logoutout, logouterr = logout.communicate()
        if logouterr:
            print "Error logging out: " + logouterr
            return 0
        elif logoutout:
            print logoutout
        
    else:
        print "Error logging out: can't find RTC executable file: " + scmfile
        return 0
    return 1
