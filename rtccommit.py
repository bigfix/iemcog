import subprocess
import re
import os

def rtc_commit(username, password, dir, comment='Committing changes', repoURL='https://rtp-rtc17.tivlab.raleigh.ibm.com:9443/jazz'):
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
    
    try:
        programFilesDir = os.environ['PROGRAMFILES(X86)']
    except:
        try:
            programFilesDir = os.environ['PROGRAMFILES']
        except:
            programFilesDir = "C:\Program Files"
    scmfile = programFilesDir + '/IBM/TeamConcert/scmtools/eclipse/scm.exe'
    
    if os.path.isfile(scmfile):
        login = subprocess.Popen([scmfile, 'login', '-r', repoURL, '-u', username, '-P', password], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        loginout, loginerr = login.communicate()
        if loginerr:
            print "Error logging in: " + loginerr
            return 0
        elif loginout:
            print loginout

        checkin = subprocess.Popen([scmfile, 'checkin', '-u', username, '-P', password, dir], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        checkinout, checkinerr = checkin.communicate()
        if checkinerr:
            print "Error checking in directory '" + dir + "': " + checkinerr
            rtc_logout(scmfile, repoURL)
            return 0
        elif checkinout:
            print checkinout

        changesetID = re.search(r'\n\s+Change sets:\s*\((\d+)\)', checkinout, re.DOTALL).group(1)
        changeset = subprocess.Popen([scmfile, 'changeset', 'comment', '-u', username, '-P', password, changesetID, comment], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        changesetout, changeseterr = changeset.communicate()
        if changeseterr:
            print "Error writing comment to changeset#" + changesetID +": " + changeseterr
            rtc_logout(scmfile, repoURL)
            return 0
        elif changesetout:
            print changesetout

        deliver = subprocess.Popen([scmfile, 'deliver', '-u', username, '-P', password, '-d', dir], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        deliverout, delivererr = deliver.communicate()
        if delivererr:
            print "Error delivering (committing) changes: " + delivererr
            rtc_logout(scmfile, repoURL)
            return 0
        elif deliverout:
            print deliverout

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